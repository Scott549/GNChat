npm run build
tar -czvf o.tar.gz dist/*
scp o.tar.gz ubuntu@172.81.241.189:/var/www/html