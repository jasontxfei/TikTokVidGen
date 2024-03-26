from TTVG import TTVG

TTVG(subreddit = 'AITA',                     # 'TIFU' or 'AITA' or 'RA', add more by changing get_posts and adding image file in Base_Images
     time_frame = 'day',                     # sorting from top's time frame
     num_ask = 25,                           # number of reddit posts to provide when choosing post
     voice = 'en_us_001',                    # 'en_us_006' (male), 'en_us_010' (male), or 'en_us_001' (female) are the classics, check voices.py for all of them
     title_voice = 'en_us_001',              # 'en_us_006' (male), 'en_us_010' (male), or 'en_us_001' (female) are the classics, check voices.py for all of them
     video_speed = 1.25,                      # video playback speed
     align_speed = 0.80,                     # slows down audio for alignment (higher accuracy)
     base_video = 'Base_Videos/sscrop.mp4',  # background video file location
     chunk_size = 350,                       # lower if you get an ffmpeg error like "autoscale" or "temp resource missing", 
                                                # this is based on ram, so 32gb ram is max 386, 16gb ram is max 180.
     fps = 60                                # fps picker, dont go more than 60 (fps of the footage)
     ).start()

