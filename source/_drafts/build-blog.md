---
title: build-blog
tags:
---
# Hexo和Markdown搭建个人博客教程🎈

在当今数字化的时代，拥有一个属于自己的个人博客是一件非常酷的事情😎。它不仅可以记录我们的生活、分享我们的知识，还能让我们结识更多志同道合的朋友。今天，我就来手把手地教大家如何使用Hexo和Markdown搭建一个属于自己的个人博客🎉。

## 一、准备工作🛠️

### 1. 注册GitHub账号
GitHub是一个代码托管平台，就像是一个巨大的代码仓库，它可以为我们提供免费的服务器和代码托管等功能👏。首先，我们需要访问GitHub官网注册一个账号。在注册的时候，一定要选择一个合适的用户名哦，因为后续博客网站的域名会用到这个名字呢😏。

注册完成后，我们来到个人主界面，点击右上角的“+”，然后选择“New repository”，创建一个名为“用户名.github.io”的仓库，比如“example.github.io”，最后点击“Create repository”就完成创建啦🥳。

### 2. 安装Git
Git是一款免费、开源的分布式版本控制系统，它就像是一个神奇的时光机，可以帮助我们将本地的Hexo内容提交到代码托管站点📡。我们需要访问Git官网，根据自己的操作系统下载对应的安装程序，然后按照提示进行安装。

安装完成后，打开命令行工具（如Windows的CMD或Git Bash），输入以下命令来配置用户名和邮箱：
```bash
git config --global user.name "你的GitHub用户名"
git config --global user.email "你的GitHub邮箱"
```

接着，我们要生成SSH密钥并添加到GitHub，这样才能在后续进行代码推送哦。输入以下命令：
```bash
ssh-keygen -t rsa -C "你的GitHub邮箱"
```
按提示一路回车，生成密钥后，找到id_rsa.pub文件（一般在C:\Users\你的用户名\.ssh目录下），使用文本编辑器打开并复制其中的内容。登录GitHub，进入“Settings” -> “SSH and GPG keys”，点击“New SSH key”，将复制的密钥内容粘贴到“Key”字段，填写标题后点击“Add SSH key”就大功告成啦🤩。

### 3. 安装Node.js和npm
Hexo是基于Node.js运行的，所以我们需要安装Node.js和它的包管理工具npm。访问Node.js官网，下载适合自己操作系统的安装包，然后按照提示进行安装。

安装完成后，打开命令行工具，输入以下命令检查安装是否成功：
```bash
node -v
npm -v
```
若显示出版本号，那就表示安装成功啦👏。为了加快后续插件下载速度，我们可以将npm的源切换为淘宝镜像，输入以下命令：
```bash
npm config set registry https://registry.npm.taobao.org
```

## 二、安装Hexo💻
在命令行工具中，使用以下命令全局安装Hexo：
```bash
npm install -g hexo-cli
```
安装完成后，输入以下命令检查Hexo是否安装成功：
```bash
hexo -v
```
若显示出版本号，就说明安装成功啦🥰。

## 三、初始化Hexo项目📂
我们要选择一个合适的目录，用来存放Hexo博客项目。在命令行中进入该目录，然后使用以下命令初始化Hexo项目：
```bash
hexo init 项目名称
cd 项目名称
npm install
```
初始化完成后，该目录下会生成一些文件和文件夹，主要包括：
- `_config.yml`：这是网站的配置信息文件，就像是博客的大脑🧠，可以对博客的各种参数进行设置。
- `package.json`：这是应用程序的信息文件，记录了项目的依赖和脚本等信息。
- `scaffolds`：这是模版文件夹，当我们新建文章时，Hexo会根据模版来建立文件。
- `source`：这是资源文件夹，用来存放我们的用户资源，比如博客文章（.md文件）、图片等。其中，`_posts`文件夹用于存放正式发布的文章，`_drafts`文件夹用于存放草稿文章。
- `themes`：这是主题文件夹，Hexo会根据主题来生成静态页面，我们可以通过更换主题来改变博客的外观哦😜。

## 四、本地预览博客👀
在项目目录下，使用以下命令生成静态文件并启动本地服务器：
```bash
hexo generate
hexo server
```
或者使用简写命令：
```bash
hexo g
hexo s
```
启动成功后，在浏览器中访问http://localhost:4000，我们就可以看到Hexo默认主题的博客页面啦🎉。如果要停止服务器，在命令行中按Ctrl + C就可以了。

## 五、安装和配置Butterfly主题🌈

### 1. 安装Butterfly主题
在Hexo项目根目录下，执行以下命令克隆Butterfly主题：
```bash
git clone -b master https://github.com/jerryc127/hexo-theme-butterfly.git themes/butterfly
```
如果没有pug以及stylus的渲染器，还需要下载安装，否则在项目运行时会报错哦。输入以下命令：
```bash
npm install hexo-renderer-pug hexo-renderer-stylus --save
```

### 2. 应用主题
我们需要修改Hexo根目录下的`_config.yml`文件，将主题设置为butterfly：
```yaml
theme: butterfly
```

### 3. 减少升级主题的不便（可选）
为了减少升级主题后带来的不便，我们可以在Hexo根目录创建一个文件`_config.butterfly.yml`，并把主题目录的`_config.yml`内容复制到`_config.butterfly.yml`中。要注意哦，我们复制的是主题的`_config.yml`，而不是Hexo的`_config.yml`，并且不要把主题目录的`_config.yml`删掉。以后只需要在`_config.butterfly.yml`进行配置就可以啦，因为Hexo会自动合并主题中的`_config.yml`和`_config.butterfly.yml`里的配置，如果存在同名配置，会使用`_config.butterfly.yml`的配置，它的优先度较高呢😎。

### 4. 主题基本配置
以下是一些常见的主题配置示例，我们可以根据自己的需求修改`_config.butterfly.yml`文件：

#### 全站设置
```yaml
# 网站总体设置
# --------------------------------------
favicon: img/favicon.png  #收藏图标
background: #设置网站背影，可设置图片或颜色
display_mode: light #网站默认的显示模式
css_prefix: true  #有些 CSS 并不是所有浏览器都支持，需要增加对应的前缀才会生效
instantpage: false # 当鼠标悬停到链接上超过 65 毫秒时会对该链接进行预加载，可以提升访问速度
```

#### 英文与汉字间插入空格
```yaml
pangu: # 在网页中所有的中文字和半形的英文、数字、符号之间插入空白
  enable: true
  field: site # site/post
```

#### 替代图片设置
```yaml
error_img: # 如果全站有图片失效，则会用以下图片替换
  flink: /img/friend_404.gif
  post_page: /img/404.jpg
```

#### 过场动画
页面打开前有一个过场的小动画，不过不太建议开启哦。
```yaml
preloader: # 过场动画
  enable: false
  source: 1 #可选值1=fullpage或2=progress bar
  pace_css_url: # (see https://codebyzach.github.io/pace/)
```

#### 404页面配置
```yaml
# A simple 404 page
error_404:
  enable: true
  subtitle: "页面沒有找到"
  background: #背景图片
```

### 5. 导航栏配置
导航栏配置可在`_config.butterfly.yml`中进行，示例如下：
```yaml
menu:
  首页: / || fas fa-home
  归档: /archives/ || fas fa-archive
  标签: /tags/ || fas fa-tags
  分类: /categories/ || fas fa-folder-open
  留言板: /messageboard/ || fa fa-paper-plane
  友链: /link/ || fa fa-link
  日志: /timeline/ || fa fa-bell
  菜单 || fa fa-list:
    - about || /about/ || fa fa-sitemap
    - myself || /myself/ || fa fa-id-card
    - butterfly || https://github.com/jerryc127/hexo-theme-butterfly/ || fa fa-heart
```

同时，我们需要创建对应的页面：

#### 标签页
```bash
hexo new page tags
```
修改`source/tags/index.md`：
```yaml
---
title: 标签
date: 2018-01-05 00:00:00
type: tags
---
```

#### 分类页
```bash
hexo new page categories
```
修改`source/categories/index.md`：
```yaml
---
title: 分类
date: 2018-01-05 00:00:00
type: categories
---
```

#### 留言板
```bash
hexo new page messageboard
```
修改`source/messageboard/index.md`：
```yaml
---
title: 留言板
date: 2018-01-05 00:00:00
type: messageboard
---
```

#### 友链
```bash
hexo new page link
```
修改`source/link/index.md`：
```yaml
---
title: 友链
date: 2018-01-05 00:00:00
type: link
---
```
在Hexo目录中的`source/_data`，创建一个文件`link.yml`，内容如下：
```yaml
class:
  class_name: 友情链接
  link_list:
    1:
      name: 姓名
      link: 链接
      avatar: 图片
      descr: 签名
    2:
      name: 姓名
      link: 链接
      avatar: 图片
      descr: 签名
```

#### 日志
```bash
hexo new page timeline
```
修改`source/timeline/index.md`：
```yaml
---
title: 日志
date: 2018-01-05 00:00:00
type: timeline
---
```

#### 关于
```bash
hexo new page about
```
修改`source/about/index.md`：
```yaml
---
title: 关于
date: 2018-01-05 00:00:00
type: about
---
```

### 6. 代码块显示设置

#### 开启代码复制功能
```yaml
highlight_copy: true
```

#### 代码框展开/关闭设置
`true`表示全部代码框不展开，需点击`>`打开；`false`表示代码框展开，有`>`点击按钮；`none`表示不显示`>`按钮。
```yaml
highlight_shrink: false #代码框展开
```

#### 代码换行设置
在默认情况下，hexo-highlight在编译的时候不会实现代码自动换行。如果我们不希望在代码块的区域里有横向滚动条，可以在`_config.butterfly.yml`中开启代码换行：
```yaml
code_word_wrap: true
```
同时，若使用highlight渲染，需要找到站点的Hexo配置文件`_config.yml`，将`line_number`改成`false`：
```yaml
highlight:
  enable: true
  line_number: false 
  auto_detect: false
  tab_replace: ''
```

## 六、配置部署信息🚀
要将本地的博客部署到GitHub上，我们需要对`_config.yml`文件进行配置。找到文件中的`deploy`字段，修改为以下内容：
```yaml
# Deployment
## Docs: https://hexo.io/docs/deployment.html
deploy:
  type: git
  repo: git@github.com:你的GitHub用户名/你的GitHub用户名.github.io.git
  branch: main
```
保存文件后，在项目目录下安装`hexo-deployer-git`插件：
```bash
npm install hexo-deployer-git --save
```

## 七、部署博客到GitHub🌐
在项目目录下，使用以下命令将博客部署到GitHub：
```bash
hexo clean
hexo generate
hexo deploy
```
或者使用简写命令：
```bash
hexo clean
hexo g
hexo d
```
部署成功后，在浏览器中访问https://你的GitHub用户名.github.io，我们就可以看到部署到GitHub上的博客页面啦🎉。

## 八、撰写和发布文章📝

### 1. 新建文章
在项目目录下，使用以下命令新建一篇文章：
```bash
hexo new "文章标题"
```
执行该命令后，会在`source/_posts`文件夹下生成一个对应的`.md`文件。

### 2. 编辑文章
我们可以使用Markdown编辑器（如Typora）打开生成的`.md`文件，编写文章内容。文章开头一般会有一些预定义参数，如标题、日期、标签、分类等，我们可以根据需要进行修改：
```yaml
---
title: 文章标题
date: 2025-05-16 16:39:18
tags: [标签1, 标签2]
categories: 分类
---
```

### 3. 发布文章
文章编写完成后，使用以下命令生成静态文件并部署到GitHub：
```bash
hexo clean
hexo generate
hexo deploy
```
或者使用简写命令：
```bash
hexo clean
hexo g
hexo d
```
部署成功后，刷新博客页面，我们就可以看到新发布的文章啦🥳。

## 九、常见问题及解决方法🙋‍♂️

### 1. 部署失败
如果在执行`hexo deploy`命令时出现`ERROR Deployer not found: git`的错误，我们可以执行以下命令安装`hexo-deployer-git`插件：
```bash
npm install hexo-deployer-git --save
```

### 2. 博客页面不显示图片
如果博客页面中的图片无法显示，我们可以进行以下设置：
- 打开`_config.yml`文件，将`post_asset_folder`字段的值设置为`true`：
```yaml
post_asset_folder: true
```
- 在项目目录下安装`hexo-asset-image`插件：
```bash
npm install https://github.com/CodeFalling/hexo-asset-image --save
```
- 将图片放在与文章同名的文件夹下，然后在文章中使用相对路径引用图片。

### 3. 无法远程访问GitHub仓库
如果第一次部署时出现无法访问GitHub仓库的情况，可能是SSH配置错误，我们需要正确配置SSH key。可以参考前面的步骤重新生成并添加SSH密钥。

### 4. DNS域名解析异常
在部署过程中，如果遇到无法将博客部署到GitHub上的情况，且通过ping命令无法ping通GitHub官网网址，则可能是出现了DNS域名解析异常。解决方法如下：
- 打开本地`C:\Windows\System32\drivers\etc\hosts`文件，在末尾添加以下命令：
```plaintext
#前者为GitHub的网址IP，后者为GitHub网址的域名
140.82.112.4        github.com
```
- 更改为国内的Gitee码云，部署方法与GitHub类似。

通过以上步骤，我们就可以成功使用Hexo和Markdown搭建一个属于自己的个人博客啦👏。希望大家都能在自己的博客里记录美好的生活，分享有价值的知识😘！