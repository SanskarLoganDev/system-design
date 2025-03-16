Explanation
VideoConsumingService:

Holds a reference to a Database instance.
The method seek_time retrieves a WatchedVideo object for a given user and video and returns its seek time.
VideoService:

Holds a reference to a FileSystem instance.
The method get_frame retrieves a Video object from the file system and then gets the specific frame based on a timestamp.
FileSystem & Database:

These classes simulate data sources. Their methods return None since no actual implementation is provided, but in a real system, they would return Video and WatchedVideo objects, respectively.
Video:

Represents a video with an identifier, a list of Frame objects, and some JSON metadata.
The get_frame method iterates over the frames and returns the one where the timestamp falls within the frame's start and end time stamps.
Frame:

Represents a video frame, with a class variable frametime analogous to a static field in Java.
Contains the frame data in bytes and its start and end timestamps.
User & WatchedVideo:

User stores user information and has a method to return the user ID.
WatchedVideo contains information about a video that a user has watched and returns the seek time.