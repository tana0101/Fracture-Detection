from ultralytics import YOLO

model = YOLO("yolo11n.pt")

train_args = {
    'data': './data/data.yaml', 
    'epochs': 300,  
    'batch': 8,    
    'device': '0', 
}

model.train(**train_args)
model.save('yolo11n_custom.pt')