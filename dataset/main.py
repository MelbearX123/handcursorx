from ultralytics import YOLO

model = YOLO("yolo11n.yaml")

if __name__ == "__main__":
    train_results = model.train(
        data="C:/Users/Steal/OneDrive/Documents/Personal_Projects/handcursorx/dataset/data.yaml",
        device=0,
        workers=1
    )