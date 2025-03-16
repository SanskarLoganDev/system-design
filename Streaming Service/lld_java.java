class VideoConsumingService {
    private Database database; // Create an instance of Database

    public int seekTime(String userId, String videoId) {
        WatchedVideo watchedVideo = database.getWatchedVideo(userId, videoId);
        return watchedVideo.getSeekTime();
    }
}

class VideoService {
    private FileSystem fileSystem;

    public VideoService(FileSystem fileSystem) {
        this.fileSystem = fileSystem;
    }

    public Frame getFrame(String videoId, int timestamp) {
        Video video = fileSystem.getVideo(videoId);
        return video.getFrame(timestamp);
    }
}

class FileSystem {
    public Video getVideo(String videoId) {
        return null;
    }
}

// Renamed `database` to `Database` and made `getWatchedVideo` a non-static method
class Database {
    public WatchedVideo getWatchedVideo(String userId, String videoId) {
        return null;
    }
}

class Video {
    String id;
    Frame[] frames;
    String jsonMetaData;
    WatchedVideo video;


    public Frame getFrame(int timestamp) {
        for (int i = 0; i < frames.length; i++) {
            if (frames[i].startTimeStamp <= timestamp &&
                frames[i].endTimeStamp > timestamp) {
                return frames[i];
            }
        }
        throw new IndexOutOfBoundsException();
    }
}

class Frame {
    public static int frametime = 10;
    byte[] bytes;
    int startTimeStamp;
    int endTimeStamp;
}

class User {
    String id;
    String name;
    String email;

    public String getId() {
        return id;
    }
}

class WatchedVideo {
    String id;
    String videoId;
    String userId;
    int seekTime;

    public int getSeekTime() {
        return seekTime;
    }
}

