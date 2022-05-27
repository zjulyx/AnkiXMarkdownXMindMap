EDITOR = """
var fields = document.getElementById("fields").children;
var codeBackgroundColor = "background-color: #414141;";
var fontFamily =
  'font-family: "Cascadia Code", "Consolas", Overpass, "GlowSansSC", "Helvetica Neue", "pingfang sc", "microsoft yahei", sans-serif;';
for (i = 0; i < 5; i++) {
  if (i === 4) {
    // code
    fields[i].children[1].shadowRoot.children[2].style =
      fontFamily + codeBackgroundColor;
  } else {
    fields[i].children[1].shadowRoot.children[2].style = fontFamily;
  }
}
"""

FRONT = """
<div class="h1 red redleft">
  <span class="redimg"><img src="_space.png" height="24" width="24" /></span>
  Question
  <span id="time"> </span>
</div>

<div class="h2 redleft wordwrap">{{Question}}</div>
"""

BACK = """
{{FrontSide}} {{#Tags}}

<div class="h1 red redleft wordwrap">[Tags] {{Tags}}</div>
{{/Tags}} {{#Mindmap}}
<hr />
<div class="slide">
  <div class="h1 green greenleft">
    <span class="greenimg"
      ><img src="_space.png" height="24" width="24"
    /></span>
    Mindmap
  </div>
  <div class="h2 greenleft">
    <svg id="mindmapgraph"></svg>
    <div id="mindmaptext" hidden>{{Mindmap}}</div>
  </div>
</div>
{{/Mindmap}} {{#Answer}}
<hr />
<div class="slide">
  <div class="h1 pink pinkleft">
    <span class="pinkimg"><img src="_space.png" height="24" width="24" /></span>
    Answer
  </div>
  <div class="h2 pinkleft wordwrap">{{Answer}}</div>
</div>
{{/Answer}} {{#Detail}}
<hr />
<div class="slide">
  <div class="h1 purple purpleleft">
    <span class="purpleimg"
      ><img src="_space.png" height="24" width="24"
    /></span>
    Detail
  </div>
  <div class="h2 purpleleft wordwrap">{{hint:Detail}}</div>
</div>
{{/Detail}} {{#Code}}
<hr />
<div class="slide">
  <div class="h1 blue blueleft">
    <span class="blueimg"><img src="_space.png" height="24" width="24" /></span>
    Code
  </div>

  <div class="h2 blueleft code wordwrap">{{Code}}</div>
</div>
{{/Code}}

<script>
  var ResourceType = {
    js: 1,
    css: 2,
  };
  loadResource("_d3@6.js", "https://cdn.jsdelivr.net/npm/d3@6", ResourceType.js)
    .then(() =>
      loadResource(
        "_markmap-lib.js",
        "https://cdn.jsdelivr.net/npm/markmap-lib",
        ResourceType.js
      )
    )
    .then(() =>
      loadResource(
        "_markmap-view.js",
        "https://cdn.jsdelivr.net/npm/markmap-view",
        ResourceType.js
      )
    )
    .then(render)
    .catch(show);

  function loadResource(path, altURL, resourceType) {
    let load = function (isLocal, resolve, reject) {
      let resource =
        resourceType === ResourceType.js
          ? document.createElement("script")
          : document.createElement("link");
      if (resourceType === ResourceType.css) {
        resource.setAttribute("rel", "stylesheet");
        resource.type = "text/css";
      }
      resource.onload = resolve;
      resource.src = isLocal ? path : altURL;
      resource.onerror = isLocal
        ? function () {
            load(false, resolve, reject);
          }
        : reject;
      document.head.appendChild(resource);
    };
    return new Promise((resolve, reject) => {
      load(true, resolve, reject);
    });
  }

  function render() {
    mindmap("mindmaptext");
    show();
  }

  function show() {
    document.getElementById("mindmapgraph").style.visibility = "visible";
  }

  function mindmap(ID) {
    if (document.getElementById("mindmapgraph").children.length === 2) {
      // Already created graph, directly return
      return;
    }
    let text = escapeHTMLChars(document.getElementById(ID).innerHTML);
    const { Markmap, loadCSS, loadJS, Transformer } = window.markmap;
    var transformer = new Transformer();
    const { root, features } = transformer.transform(text);
    const { styles, scripts } = transformer.getUsedAssets(features);
    if (styles) loadCSS(styles);
    if (scripts) loadJS(scripts, { getMarkmap: () => window.markmap });
    Markmap.create("#mindmapgraph", null, root);
  }
  function escapeHTMLChars(str) {
    return str
      .replace(/<[\/]?pre[^>]*>/gi, "")
      .replace(/<br\s*[\/]?[^>]*>/gi, "\\n")
      .replace(/<br\s*[\/]?[^>]*>/gi, "\\n")
      .replace(/<[\/]?span[^>]*>/gi, "")
      .replace(/<ol[^>]*>/gi, "")
      .replace(/<\/ol[^>]*>/gi, "\\n")
      .replace(/<ul[^>]*>/gi, "")
      .replace(/<\/ul[^>]*>/gi, "\\n")
      .replace(/<div[^>]*>/gi, "")
      .replace(/<\/div[^>]*>/gi, "\\n")
      .replace(/<li[^>]*>/gi, "- ")
      .replace(/<\/li[^>]*>/gi, "\\n")
      .replace(/&nbsp;/gi, " ")
      .replace(/&tab;/gi, "	")
      .replace(/&gt;/gi, ">")
      .replace(/&lt;/gi, "<")
      .replace(/&amp;/gi, "&");
  }
</script>
"""

CSS = """
  @font-face {
    font-family: "Cascadia Code";
    src: url("_CascadiaCode.ttf");
  }
  .card {
    font: 20px/30px yh;
    background-color: white;
    text-align: left;
  }
  
  .h1 {
    font: 22px/22px yh;
    padding: 0.3em 0em 0.3em 0.5em;
    font-family: "Cascadia Code", "Consolas", Overpass, "GlowSansSC", "Helvetica Neue",
      "pingfang sc", "microsoft yahei", sans-serif;
  }
  .h2 {
    font: 20px/30px yh;
    padding: 0.3em 0em 0.3em 0.5em;
    font-family: "Cascadia Code", "Consolas", Overpass, "GlowSansSC", "Helvetica Neue",
      "pingfang sc", "microsoft yahei", sans-serif;
  }
  
  code {
    font-family: "Cascadia Code", "Courier New", "Consolas", Overpass,
      "GlowSansSC", "Helvetica Neue", "pingfang sc", "microsoft yahei", sans-serif;
  }
  
  .redleft {
    border-left: 3px solid #ec6c4f;
  }
  .blueleft {
    border-left: 3px solid #338eca;
  }
  .pinkleft {
    border-left: 3px solid #d4237a;
  }
  .greenleft {
    border-left: 3px solid #9acd32;
  }
  .purpleleft {
    border-left: 3px solid #594d9c;
  }
  
  .code {
    background-color: #414141;
    font-family: "Cascadia Code", "Consolas", Overpass, "GlowSansSC",
      "Helvetica Neue", "pingfang sc", "microsoft yahei", sans-serif;
  }
  
  .wordwrap {
    display: block;
    word-wrap: break-word;
  }
  
  .red {
    color: #ec6c4f;
  }
  .blue {
    color: #338eca;
  }
  .green {
    color: #9acd32;
  }
  .pink {
    color: #d4237a;
  }
  .purple {
    color: #594d9c;
  }
  
  .redimg {
    background: url(_red-day.svg);
    background-size: 100%;
    background-repeat: no-repeat;
    background-position: center;
  }
  .blueimg {
    background: url(_blue-day.svg);
    background-size: 100%;
    background-repeat: no-repeat;
    background-position: center;
  }
  .pinkimg {
    background: url(_pink-day.svg);
    background-size: 100%;
    background-repeat: no-repeat;
    background-position: center;
  }
  .greenimg {
    background: url(_green-day.svg);
    background-size: 100%;
    background-repeat: no-repeat;
    background-position: center;
  }
  .purpleimg {
    background: url(_purple-day.svg);
    background-size: 100%;
    background-repeat: no-repeat;
    background-position: center;
  }
  
  .hint {
    color: black;
  }
  
  a {
    color: #666;
  }
  img {
    max-width: 100%;
    vertical-align: middle;
  }
  .chrome img {
    max-width: 100%;
    vertical-align: middle;
  }
  ul,
  ol {
    margin-top: 0em;
  }
  ul li {
    margin-left: -0.9em;
  }
  i {
    padding: 0 3px 0 0;
  }
  u {
    text-decoration: none;
    background-color: #ffff75;
    border-bottom: 2px solid #ec6c4f;
  }
  hr {
    height: 1px;
    width: 100%;
    display: block;
    border: 0px solid #fff;
    margin: 5px 0px 10px 0px;
    background-color: #ccc;
  }
  
  #answer, #mindmapgraph {
      visibility: hidden;
  }

  #mindmapgraph{
    height: 50vh;
    width: 95vw;
  }
  
  .markmap-foreign {
    font: 16px/20px "Cascadia Code", "Consolas", Overpass, "GlowSansSC", "Helvetica Neue",
      "pingfang sc", "microsoft yahei", sans-serif;
  }
"""
