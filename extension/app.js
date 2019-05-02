'use strict';



document.addEventListener('DOMContentLoaded', function() {
   var expression = $("#cwos").clone();
   var result = $(".vUGUtc").clone();
   function animate() {

      let element = $("div#cwmcwd.vk_c.card-section");
      /*element.animate({
         left: '250px',
         opacity: '0.4',
      },
      "slow"
      );*/
      element.children("div").fadeToggle(200);
      $("div#soso1").toggleClass("hdtb-msel");
      $("div.hdtb-mitem:first-child").toggleClass("hdtb-msel");

      if ($("#soso").text() == "Close")
         $("#soso").text("Shows")
      else
         $("#soso").text("Close");

      console.log(result.text());
      console.log(expression.text());
      $("#new").html(`<h3>Expression: ${expression[0].innerHTML}</h3>
                     <h3>Expression: ${result[0].innerHTML}</h3>
                     <hr/>
							<form id="form-send"action = "https://localhost:5000/upload?exp=${expression.text()}&res=${result.text()}" method = "POST" enctype = "multipart/form-data">
							<input type = "file" name = "file" />
							<input type = "hidden" name = "exp" id="exp" value="${expression.text()}"/>
							<input type = "hidden" name = "res" id="exp" value="${result.text()}"/>
							<input type = "submit"/>
                  </form>
                  <div id="show-here"></div>`);
      fetch(`https://localhost:5000/find?exp=${expression.text()}&res=${result.text()}`).then(response => response.json()).then(json => {
               $.each(json.files, function() {
                  var new_file = `<tr>
                     <td>
                        <a href="${this.url}" title="${this.name}" download="${this.name}" data-gallery><img src="${this.thumbnailUrl}"/></a>
                     </td>
                     <td>
                        <p>
                           <a href="${this.url}" title="${this.name}"download ="${this.name}">${this.name}</a>
                        </p>
                     </td>
                     <td>
                         <span class="size">${this.size}</span>
                     </td>
                     <td>
                        <button data-type="${this.type}" data-url="${this.deleteUrl}">delete</button>
                     </td>
                  </tr>`
                  $("#show-here").append(new_file);
                });
            });
   }

   if(document.getElementsByClassName("vUGUtc")){
      function execute() {
         expression = $("#cwos").clone();
         result = $(".vUGUtc").clone();
         result.find("*").removeAttr("jsname class style id");
         expression.find("*").removeAttr("jsname class style id");
         result.removeAttr("class style id");
         expression.removeAttr("class style id");

         expression.unwrap();
         result.unwrap();

         console.log(result[0]);
         console.log(expression[0]);

         animate();

      }
      if(document.getElementById("cwos")){
         let $input = $('<div aria-selected="false" class="hdtb-mitem hdtb-imb" id="soso1" role="tab"><a  id="soso" class="q qs" href="#">Shows</a></div>').click(execute);
         console.log("button created")
         jQuery("#hdtb-msb-vis").append($input);

         let element = $("div#cwmcwd.vk_c.card-section");
         element.append('<div id="new" style="display:none;"></div>');
      }
   }
});