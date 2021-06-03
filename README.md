# facial-mask-detection-and-surveillance
Real-time face mask detection with facial recognition. The program detects whether if someone is wearing a mask or not with the video stream. 
If a person is found to be not wearing any face mask, a snapshot of that person will be taken, and facial recognition will be done on the snapshot to identify the identity of the person.
The information will then be be added into a spreadsheert report.
The authorities may then use the information collected in the spreadsheet to send out warnings to people who are caught not wearing any masks.

# Requirements
pip install opencv-python

pip install numpy

pip install tensorflow

pip install scikit-learn

pip install imutils

pip install matplotlib

pip install numpy

# Dataset links for masked and unmasked face sets
Contains two folders of masked and unmasked datasets. Simple place the pictures into the masked and without mask folder in the project file will do.
https://bit.ly/34Gh5ab

Credits to Maskedface-Net for the no mask and masked dataset to train the model:
https://github.com/cabani/MaskedFace-Net

# How-to
1. Input your datasets into the folder.
2. Run the train_mask_detector.py to train the model with the loaded dataset.
3. Run the detect_mask_video.py to start the face mask recognition through your webcam.
4. If you are not wearing any mask for more than 3 seconds, the program will take a snapshot.
5. Run the detect_mask_photo to detect any face mask worn in a picture.
6. Input any face data with the person's name as the image's name in the face_ID folder.
7. Run the anti_masker_identifier to detect the person not wearing a mask in the snapshot folder.
8. Check the report.csv .
