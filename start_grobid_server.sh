sudo docker run -t --rm --init -p 8080:8070 -p 8081:8071 -v /home/ishaq/Desktop/personal-projects/rename-scientific-publications/config.yaml:/opt/grobid/grobid-service/config/config.yaml:ro lfoppiano/grobid:0.6.2
