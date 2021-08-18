# Application Views
Classes in this folder act as the views for Flask and expose the application
to the network. Extension of the API should happen here and new classes
introduced should inherit from BaseClip.
Here, the concept of Clip is introduced used throughout the whole project.
A clip is the representation of an object in the clipboard. Apart from its
data it must contain a mimetype. Several other pieces of data can be sent
with custom HTTP-headers. Please refer to parser.py for a specification
of those.
Apart from Recipient, the classes were added to split the logic of processing
the incoming data into different methods as to make the code more readable.