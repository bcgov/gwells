<template>
    <div id="topicTemplate" class="template container gov-container">
        <div id="breadcrumbContainer">
            <ol class="breadcrumb">

                <li>
                    <a href="#">Home</a>
                </li>
                <li>
                    <a href="#">Breadcrumb Link</a>
                </li>
                <li>
                    <a href="#">Breadcrumb Link</a>
                </li>
                <li>
                    <a href="#">Breadcrumb Link</a>
                </li>
            </ol>
        </div>
        <div class="row">
            <div id="main-content" role="main" class="contentPageMainColumn col-sm-12">
                <a id="main-content-anchor"></a>
                <h1>Heading Style 1 Single Column Layout</h1>
                <div id="introduction"></div>
                    <p>Insert your introductory content here. Ensure your content meets the stylistic and formatting standards for writing consistent and high quality content for B.C. government websites.</p>
                </div>
                <div id="body">
                    <h2>Heading Style 2</h2>
                    <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</p>

                    <p>"At vero eos et accusamus et iusto odio dignissimos ducimus qui blanditiis praesentium voluptatum deleniti atque corrupti quos dolores et quas molestias excepturi sint occaecati cupiditate non provident, similique sunt in culpa qui officia deserunt mollitia animi, id est laborum et dolorum fuga. Et harum quidem rerum facilis est et expedita distinctio. Nam libero tempore, cum soluta nobis est eligendi optio cumque nihil impedit quo minus id quod maxime placeat facere possimus, omnis voluptas assumenda est, omnis dolor repellendus. Temporibus autem quibusdam et aut officiis debitis aut rerum necessitatibus saepe eveniet ut et voluptates repudiandae sint et molestiae non recusandae. Itaque earum rerum hic tenetur a sapiente delectus, ut aut reiciendis voluptatibus maiores alias consequatur aut perferendis doloribus asperiores repellat."</p>

                    <ul>
                        <li><a href="#" target="_self">Abbreviations</a>&nbsp;</li>
                        <li><a href="#" target="_self">Capitalization</a></li>
                        <li><a href="#" target="_self">Formatting</a></li>
                        <li><a href="#" target="_self">Headings</a></li>
                        <li><a href="#" target="_self">Links</a></li>
                        <li><a href="#" target="_self">Lists</a></li>
                        <li><a href="#" target="_self">Numbers &amp; Dates</a></li>
                        <li><a href="#" target="_self">Plain Language</a></li>
                        <li><a href="#" target="_self">Punctuation</a></li>
                        <li><a href="#" target="_self">Word Usage</a></li>
                    </ul>
                </div>
            </div>
        </div>
</template>

<script>
export default {
  name: 'HelloWorld',
  data () {
    return {
      msg: 'Welcome to Your Vue.js App'
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1, h2 {
  font-weight: normal;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
