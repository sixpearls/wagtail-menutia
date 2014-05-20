IE_submenu_fix = function() {
    if (document.all&&document.getElementById) {
        navRoot = document.getElementById("menu-nav-menu");
        for (i=0; i<navRoot.childNodes.length; i++) {
            node = navRoot.childNodes[i];
            if (node.nodeName=="LI") {
                node.onmouseover=function() {
                    this.className+=" over";
                }
                node.onmouseout=function() {
                    this.className=this.className.replace(" over", "");
                }
            }
        }
   }
}
window.onload=IE_submenu_fix;

$(function() { //create select drop down for small screens
    // Create the dropdown base
    function parseMenu(ul_element,prefix_in,select_el) {
        var select = select_el;
        var prefix = prefix_in;

        // Populate dropdown with menu items
        $(ul_element).children("li").each(function(index,element) {

            var a_el = $(element).children("a");
            var menuText = prefix + a_el.text();

            if (a_el.length > 0) {

                $("<option />", {
                        "value"   : a_el.attr("href"),
                        "text"    : menuText
                }).appendTo(select);

            }

            $(element).children('ul').each(function(index, element) {
                parseMenu(element,prefix+' - ',select)
            });
             
        });
    }

    $("nav > ul").each( function(index, element) {
        var select = $("<select />").appendTo(element.parentElement);
        // Create default option "Go to..."
        $("<option />", {
         "selected": "selected",
         "value"   : "",
         "text"    : "Go to..."
        }).appendTo(select);

        parseMenu(element,'',select);
        // To make dropdown actually work
        // To make more unobtrusive: http://css-tricks.com/4064-unobtrusive-page-changer/
        $(select).change(function() {
        window.location = $(this).find("option:selected").val();
        });
    });

});
