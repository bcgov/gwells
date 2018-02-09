newman run apitest.json -r html,cli,junit
mv newman/*.html newman/index.html

