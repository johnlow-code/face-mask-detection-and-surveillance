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
Contains two folders of masked and unmasked datasets. Simple place the pictures in to the masked and without mask folder in the project file will do.

https://bit.ly/34Gh5ab

Credits to Maskedface-Net for the no mask and masked dataset to train the model:
https://github.com/cabani/MaskedFace-Net
