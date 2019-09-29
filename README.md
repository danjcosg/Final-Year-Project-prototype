# Facial Attributes and Facial Recognition: An Investigation
If we wanted to build an automatic summary system for videos, we would need to be able to detect when the characters appear in a film. This was the motivation for my dissertation. This repository contains the code I used to investigate how changing attributes of a face (eg: pose, lighting, facial hair) affect recognition, using modern recognition techniques. 

# Overview
[Overview document.](https://docs.google.com/presentation/d/1URz-3HzZ5AuwvxX-urZ1Ym7lGgBGjNM26xOgB3kEp8M/edit?usp=sharing)

# Key Words & Libraries

Face Detection - Detection of a face in an image.

Face Recognition - Mapping of a face to a name.

DLib - Machine Learning Library.

FIQ (Face Image Quality) - A metric representing how suitable an image of a face is as a reference for a Face Recognition System.


# Findings
##5 Conclusion
The examples from the previous section have revealed how for three attributes, (glasses,
facial expression, illumination):

1. these attributes gave an unexpected and large superiority in FIQ to images from set B.
2. These increases were generally only present when the corresponding target face had
the same attribute.

My conclusion is that , while some attribute values are always worse (see Section 4.3 results for sebastian Stan), the highest quality reference image is actally context-dependent. For example, glasses neither positively nor
negatively affected FIQ. Instead it would be better to say face A without glasses is of
highest quality in cases where glasses are not present. Face B with glasses is of highest
quality in cases where glasses are present: 

For neural network classifiers, the space of Face Image Quality has many equivalent peaks, and must include the target face as a parameter to be well defined:

>For modern systems searching over unconstrained faces, for a given attribute x, FIQ is positively affected by the input face sharing the same value of x as the target face.

>For an input face with a set of attributes A, FIQ is highest when A is also the set of
attributes of the target face.

## Future Work
Further experiments could measure how FIQ varies for attributes not tested in this
project (eg: presence of sunglasses, hairstyle). As well as this the hypothesis could be
further validated or refuted by repeating this project’s methodology with more carefully
selected and larger input data. An interesting follow up
experiment would be to test the extent to which attributes can be doctored in an image, and
whether these forgeries could improve the diversity of the input data (and hence FIQ).
Generative Adversarial Networks may be ideal for such work, so as to forge as realistic an
attribute as possible.
