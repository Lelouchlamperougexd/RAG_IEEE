import argparse
from src import data_preparation, model_training, model_evaluation, model_inference

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Запуск проекта")
    parser.add_argument("mode", choices=["prepare", "train", "evaluate", "infer"], help="Режим работы")
    args = parser.parse_args()

    if args.mode == "prepare":
        data_preparation.prepare_data()
    elif args.mode == "train":
        model_training.train_models()
    elif args.mode == "evaluate":
        model_evaluation.evaluate_models()
    elif args.mode == "infer":
        model_inference.run_inference()