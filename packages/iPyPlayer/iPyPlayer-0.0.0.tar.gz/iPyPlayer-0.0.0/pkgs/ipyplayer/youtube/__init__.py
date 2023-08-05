
import dataengineer as de
de.conf.ProjectInfo.set('ProjectName', 'YouTubePlayer')
de.conf.Database.set('name', 'YouTubePlayer')
de.conf.show()
from youtube.youtube import *
