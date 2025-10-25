import os


def main():
    while True:
        print("\nWelcome to AURA Prototype Launcher\n")
        print("Please choose a module to run:")
        print("1. Speech Recognition")
        print("2. Gesture-to-Speech AAC")
        print("3. Speech Error Classification")
        print("4. Adaptive Therapy (GUI Scheduler)")
        print("0. Exit\n")

        choice = input("Enter your choice: ")

        if choice == "1":
            os.system("python speech_recognition/wav2vec2_recognizer.py")

        elif choice == "2":
            os.system("python multimodal_aac_enhanced/gesture_to_speech_gui.py")

        elif choice == "3":
            print("\nRunning Speech Error Classification...")
            os.system("python error_classification/log_predictions.py")
            print("✅ Predictions saved to CSV.")

            launch_gui = input("Launch Adaptive Therapy GUI now? (y/n): ").lower()
            if launch_gui == "y":
                os.system("python error_classification/adaptive_therapy_gui.py")

        elif choice == "4":
            os.system("python error_classification/adaptive_therapy_gui.py")

        elif choice == "0":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
