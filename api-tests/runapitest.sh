npm install newman
newman run apitest.json -r html,cli,junit
cd newman
mv *.html index.html
cd ..


