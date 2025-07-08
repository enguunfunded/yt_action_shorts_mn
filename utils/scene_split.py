# utils/scene_split.py
import subprocess

def detect_action_scenes(video_path, min_duration=10, max_clips=10):
    """
    PySceneDetect ашиглан кадр солигдсон хэсгүүдийг илрүүлж,
    action ихтэй хэсгүүдээс 10 орчим клип буцаана.
    """
    import scenedetect
    from scenedetect import VideoManager, SceneManager
    from scenedetect.detectors import ContentDetector

    video_manager = VideoManager([video_path])
    scene_manager = SceneManager()
    scene_manager.add_detector(ContentDetector(threshold=30.0))

    base_timecode = video_manager.get_base_timecode()
    video_manager.set_downscale_factor()
    video_manager.start()

    scene_manager.detect_scenes(frame_source=video_manager)
    scene_list = scene_manager.get_scene_list(base_timecode)

    # Scene хугацааг секундээр буцаана
    scenes_sec = [(scene[0].get_seconds(), scene[1].get_seconds()) for scene in scene_list]
    valid_scenes = [(s, e) for s, e in scenes_sec if e - s >= min_duration]

    # Clip-г санамсаргүйгээр эсвэл эхнээс нь хязгаарлана
    return valid_scenes[:max_clips]
