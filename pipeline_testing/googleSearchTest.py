from google_images_download import google_images_download
import sys

#possible arguemnts for the search query. If you don't want a particular argument to be searched, just input an empty string ""
try:
	params = {'actor_name' : sys.argv[1], 'character_name' : sys.argv[2], 'movie_title' : sys.argv[3],  'headshot' : sys.argv[4] }
except:
	print('An error occured. 4 arguments are required: \n\t<actor name> <character name> <movie title> <headshot>. \n\t\t If you don\'t want a particular argument to be searched, just input an empty string: ""')
query = ""

#this is only required if the arguments passed contain the quotation marks
for k, s in params.items():
	print(s)
	if len(s) > 2:
		if s[0] == '"' and s[len(s)-1] == '"':
			s = s[1:len(s) - 1]
	query += ' ' + s

print("|"+query+"|")
response = google_images_download.googleimagesdownload()
absolute_image_paths = response.download({"keywords":"{}".format(query), "output_directory":"./face_downloads" ,"limit":20})
