"""Train and export a backend-compatible plant disease classifier.

Usage examples
--------------
One command with an already split dataset:
    python scripts/train_plant_disease.py --data-dir data/raw/PlantVillage

One command with a custom output path:
    python scripts/train_plant_disease.py --data-dir data/raw/PlantVillage --output models/vision/plant_disease.pt

Expected dataset formats
------------------------
1. Split format:
   data-dir/
       train/
           class_a/
           class_b/
       val/
           class_a/
           class_b/

2. Unsplit format:
   data-dir/
       class_a/
       class_b/

If train/ and val/ are missing, the script creates an 80/20 split automatically.
The exported checkpoint includes model_state, model_name, num_classes, and class_names,
which matches what the API loads through VisionModel.load().
"""

from __future__ import annotations

import argparse
import math
import random
from pathlib import Path

import torch
from torch import nn
from torch.utils.data import DataLoader, random_split
from torchvision import datasets, transforms

from src.vision.model import VisionModel


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train a plant disease classifier and export plant_disease.pt")
    parser.add_argument("--data-dir", required=True, help="PlantVillage root directory")
    parser.add_argument("--output", default="models/vision/plant_disease.pt", help="Checkpoint output path")
    parser.add_argument("--model-name", default="efficientnet_v2_s", choices=["efficientnet_v2_s", "vit_b16"])
    parser.add_argument("--epochs", type=int, default=5)
    parser.add_argument("--batch-size", type=int, default=16)
    parser.add_argument("--learning-rate", type=float, default=1e-4)
    parser.add_argument("--val-split", type=float, default=0.2)
    parser.add_argument("--seed", type=int, default=42)
    return parser.parse_args()


def build_transforms() -> tuple[transforms.Compose, transforms.Compose]:
    train_transform = transforms.Compose(
        [
            transforms.Resize((256, 256)),
            transforms.RandomResizedCrop(224),
            transforms.RandomHorizontalFlip(),
            transforms.RandomRotation(10),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ]
    )
    eval_transform = transforms.Compose(
        [
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ]
    )
    return train_transform, eval_transform


def load_datasets(data_dir: Path, val_split: float, seed: int):
    train_transform, eval_transform = build_transforms()
    train_dir = data_dir / "train"
    val_dir = data_dir / "val"

    if train_dir.is_dir() and val_dir.is_dir():
        train_dataset = datasets.ImageFolder(train_dir, transform=train_transform)
        val_dataset = datasets.ImageFolder(val_dir, transform=eval_transform)
        class_names = train_dataset.classes
        if class_names != val_dataset.classes:
            raise ValueError("Train and val class folders do not match.")
        return train_dataset, val_dataset, class_names

    base_dataset = datasets.ImageFolder(data_dir, transform=train_transform)
    class_names = base_dataset.classes
    val_size = max(1, math.floor(len(base_dataset) * val_split))
    train_size = len(base_dataset) - val_size
    generator = torch.Generator().manual_seed(seed)
    train_subset, val_subset = random_split(base_dataset, [train_size, val_size], generator=generator)

    eval_dataset = datasets.ImageFolder(data_dir, transform=eval_transform)
    val_subset.dataset = eval_dataset
    return train_subset, val_subset, class_names


def evaluate(model: VisionModel, loader: DataLoader, criterion: nn.Module, device: str) -> tuple[float, float]:
    model.model.eval()
    total_loss = 0.0
    total_correct = 0
    total_samples = 0

    with torch.no_grad():
        for images, labels in loader:
            images = images.to(device)
            labels = labels.to(device)
            logits = model.model(images)
            loss = criterion(logits, labels)
            predictions = logits.argmax(dim=1)
            total_loss += loss.item() * images.size(0)
            total_correct += (predictions == labels).sum().item()
            total_samples += images.size(0)

    return total_loss / total_samples, total_correct / total_samples


def train(args: argparse.Namespace) -> Path:
    random.seed(args.seed)
    torch.manual_seed(args.seed)

    data_dir = Path(args.data_dir)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    train_dataset, val_dataset, class_names = load_datasets(data_dir, args.val_split, args.seed)
    train_loader = DataLoader(train_dataset, batch_size=args.batch_size, shuffle=True, num_workers=0)
    val_loader = DataLoader(val_dataset, batch_size=args.batch_size, shuffle=False, num_workers=0)

    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = VisionModel(
        model_name=args.model_name,
        num_classes=len(class_names),
        pretrained=True,
        device=device,
        class_names=class_names,
    )

    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.model.parameters(), lr=args.learning_rate)

    best_val_accuracy = 0.0
    best_state = None

    for epoch in range(1, args.epochs + 1):
        model.model.train()
        running_loss = 0.0
        running_correct = 0
        running_samples = 0

        for images, labels in train_loader:
            images = images.to(device)
            labels = labels.to(device)

            optimizer.zero_grad()
            logits = model.model(images)
            loss = criterion(logits, labels)
            loss.backward()
            optimizer.step()

            predictions = logits.argmax(dim=1)
            running_loss += loss.item() * images.size(0)
            running_correct += (predictions == labels).sum().item()
            running_samples += images.size(0)

        train_loss = running_loss / running_samples
        train_accuracy = running_correct / running_samples
        val_loss, val_accuracy = evaluate(model, val_loader, criterion, device)

        print(
            f"Epoch {epoch}/{args.epochs} | "
            f"train_loss={train_loss:.4f} train_acc={train_accuracy:.4f} | "
            f"val_loss={val_loss:.4f} val_acc={val_accuracy:.4f}"
        )

        if val_accuracy >= best_val_accuracy:
            best_val_accuracy = val_accuracy
            best_state = {key: value.detach().cpu() for key, value in model.model.state_dict().items()}

    if best_state is not None:
        model.model.load_state_dict(best_state)

    model.save(str(output_path))
    print(f"Saved checkpoint to: {output_path}")
    print(f"Best validation accuracy: {best_val_accuracy:.4f}")
    return output_path


if __name__ == "__main__":
    train(parse_args())
