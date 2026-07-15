import os
import json
import shutil
import markdown

inputDir = "src/posts"
outputDir = "dist"
assetsDir = "src/assets"
postTemplateDir = "src/templates/post.html"
jsonPostDataDir = "dist/posts.json"

with open(postTemplateDir) as f:
    postTemplate = f.read()

posts = []

if os.path.exists(outputDir):
    shutil.rmtree(outputDir)
os.makedirs(f"{outputDir}/posts", exist_ok=True)

shutil.copytree(assetsDir, f"{outputDir}/assets", dirs_exist_ok=True)
shutil.copy("src/templates/home.html", f"{outputDir}/index.html")

for fileName in os.listdir(inputDir):
    with open(f"{inputDir}/{fileName}", "r") as f:
        title = f.readline().removeprefix("# ")
    slug = fileName.removesuffix(".md")
    url = f"/posts/{slug}"
    posts.append({"title": title.strip(), "slug": slug, "url": url})

for i in range(len(posts)):
    with open(f"{inputDir}/{posts[i]['slug']}.md") as f:
        lines = f.read().splitlines()
    body = "\n".join(lines[1:])
    html_content = markdown.markdown(body)
    output = postTemplate.replace("{{content}}", html_content)
    output = output.replace("{{title}}", posts[i]["title"])
    output = output.replace("{{slug}}", posts[i]["slug"])

    output = output.replace("{{leftHref}}", posts[(i-1) % len(posts)]["url"])
    output = output.replace("{{rightHref}}", posts[(i+1) % len(posts)]["url"])

    output = output.replace("{{leftText}}", posts[(i-1) % len(posts)]["title"])
    output = output.replace("{{rightText}}", posts[(i+1) % len(posts)]["title"])

    with open(f"{outputDir}/posts/{posts[i]['slug']}.html", 'w') as f:
        f.write(output)

with open(jsonPostDataDir, "w") as f:
    f.write(json.dumps(posts, indent=4, sort_keys=True))