class VideoConsumingService:
    def __init__(self, database):
        self.database = database

    def seek_time(self, user_id, video_id):
        watched_video = self.database.get_watched_video(user_id, video_id)
        return watched_video.get_seek_time()


class VideoService:
    def __init__(self, file_system):
        self.file_system = file_system

    def get_frame(self, video_id, timestamp):
        video = self.file_system.get_video(video_id)
        return video.get_frame(timestamp)


class FileSystem:
    def get_video(self, video_id):
        # In a real implementation, this method would return a Video object
        return None


class Database:
    def get_watched_video(self, user_id, video_id):
        # In a real implementation, this method would query a database and return a WatchedVideo object
        return None


class Video:
    def __init__(self, video_id, frames, json_meta_data):
        self.id = video_id
        self.frames = frames  # Expecting a list of Frame objects
        self.json_meta_data = json_meta_data

    def get_frame(self, timestamp):
        for frame in self.frames:
            if frame.start_time_stamp <= timestamp < frame.end_time_stamp:
                return frame
        # If no frame is found, raise an error similar to Java's IndexOutOfBoundsException
        raise IndexError("No frame found for the given timestamp")


class Frame:
    frametime = 10  # Class variable equivalent to a static field in Java

    def __init__(self, bytes_, start_time_stamp, end_time_stamp):
        self.bytes = bytes_  # bytes (or bytearray) representing the frame data
        self.start_time_stamp = start_time_stamp
        self.end_time_stamp = end_time_stamp


class User:
    def __init__(self, user_id, name, email):
        self.id = user_id
        self.name = name
        self.email = email

    def get_id(self):
        return self.id


class WatchedVideo:
    def __init__(self, watched_video_id, video_id, user_id, seek_time):
        self.id = watched_video_id
        self.video_id = video_id
        self.user_id = user_id
        self.seek_time = seek_time

    def get_seek_time(self):
        return self.seek_time
