//for refresh button in the homecal html
function clearAll() {
    document.getElementById('liveAlertPlaceholder').innerHTML = null;
    document.getElementById('total').value = 0;
    document.getElementById('itemName').value = '';
    document.getElementById('itemQuantity').value = '';
  }
//for refresh button in the homecal html END
//total reducer

function reduce(item_name,quantity) {
  const itemValue = parseInt(dataV[dataN.indexOf(item_name)]);
  const total_value = parseInt(document.getElementById('total').value);
  document.getElementById('total').value = total_value-(itemValue*quantity);
  delete inputData[item_name];
  QandN(inputData);
}
//total reducer END

//for filtering value
function QandN(dataObj) {
  let textN='';
  let textQ='';
  for (let i in dataObj){
    textN += i+'+';
    textQ += dataObj[i]+'+';
  }
  document.getElementById('itemName').value = textN;
  document.getElementById('itemQuantity').value = textQ;
}
//for filteirng value END

//data building 
function addData(name,quantity){
  inputData[name]=quantity;
  // if (name in inputData){
  //   nQ = inputData[name]+quantity;
  //   inputData[name] = nQ;
  // }else{
  //   inputData[name]=quantity;
  // } 
}

// for filtering item_name
function name_filter(data) {
    var name_list = [];
    for ( let x=0;x<=data.length-1;x++){
        value = data[x]['item_name'];
        name_list.push(value);
    }
    return name_list
}
// for filtering item_name END

//autocomplete function
function autocomplete(inp, arr) {
    /*the autocomplete function takes two arguments,
    the text field element and an array of possible autocompleted values:*/
    var currentFocus;
    /*execute a function when someone writes in the text field:*/
    inp.addEventListener("input", function(e) {
        var a, b, i, val = this.value;
        /*close any already open lists of autocompleted values*/
        closeAllLists();
        if (!val) { return false;}
        currentFocus = -1;
        /*create a DIV element that will contain the items (values):*/
        a = document.createElement("DIV");
        a.setAttribute("id", this.id + "autocomplete-list");
        a.setAttribute("class", "autocomplete-items");

        //testing......
        /*append the DIV element as a child of the autocomplete container:*/
        this.parentNode.appendChild(a);
        /*for each item in the array...*/
        for (i = 0; i < arr.length; i++) {
          /*check if the item starts with the same letters as the text field value:*/
          if (arr[i].substr(0, val.length).toUpperCase() == val.toUpperCase()) {
            /*create a DIV element for each matching element:*/
            b = document.createElement("DIV");
            //tesing..............
            /*make the matching letters bold:*/
            b.innerHTML = "<strong>" + arr[i].substr(0, val.length) + "</strong>";
            b.innerHTML += arr[i].substr(val.length);
            /*insert a input field that will hold the current array item's value:*/
            b.innerHTML += "<input type='hidden' value='" + arr[i] + "'>";
            /*execute a function when someone clicks on the item value (DIV element):*/
            //b.style.backgroundColor = "red";
            b.addEventListener("click", function(e) {
                /*insert the value for the autocomplete text field:*/
                inp.value = this.getElementsByTagName("input")[0].value;
                /*close the list of autocompleted values,
                (or any other open lists of autocompleted values:*/
                closeAllLists();
            });
            a.appendChild(b);
          }
        }
    });
    /*execute a function presses a key on the keyboard:*/
    inp.addEventListener("keydown", function(e) {
        var x = document.getElementById(this.id + "autocomplete-list");
        if (x) x = x.getElementsByTagName("div");
        if (e.keyCode == 40) {
          /*If the arrow DOWN key is pressed,
          increase the currentFocus variable:*/
          currentFocus++;
          /*and and make the current item more visible:*/
          addActive(x);
        } else if (e.keyCode == 38) { //up
          /*If the arrow UP key is pressed,
          decrease the currentFocus variable:*/
          currentFocus--;
          /*and and make the current item more visible:*/
          addActive(x);
        } else if (e.keyCode == 13) {
          /*If the ENTER key is pressed, prevent the form from being submitted,*/
          e.preventDefault();
          if (currentFocus > -1) {
            /*and simulate a click on the "active" item:*/
            if (x) x[currentFocus].click();
          }
        }
    });
    function addActive(x) {
      /*a function to classify an item as "active":*/
      if (!x) return false;
      /*start by removing the "active" class on all items:*/
      removeActive(x);
      if (currentFocus >= x.length) currentFocus = 0;
      if (currentFocus < 0) currentFocus = (x.length - 1);
      /*add class "autocomplete-active":*/
      x[currentFocus].classList.add("autocomplete-active");
    }
    function removeActive(x) {
      /*a function to remove the "active" class from all autocomplete items:*/
      for (var i = 0; i < x.length; i++) {
        x[i].classList.remove("autocomplete-active");
      }
    }
    function closeAllLists(elmnt) {
      /*close all autocomplete lists in the document,
      except the one passed as an argument:*/
      var x = document.getElementsByClassName("autocomplete-items");
      for (var i = 0; i < x.length; i++) {
        if (elmnt != x[i] && elmnt != inp) {
          x[i].parentNode.removeChild(x[i]);
        }
      }
    }
    /*execute a function when someone clicks in the document:*/
    document.addEventListener("click", function (e) {
        closeAllLists(e.target);
    });
}

//for deleting option
function displayNO() {
  document.getElementById('test').innerHTML = "work";
  //document.getElementById('second').style.display = "block";
}

//for registering in password hover
function mouseOver(){
  document.getElementById('pswdList').style.display="inline";
}
function mouseOut(){
  document.getElementById('pswdList').style.display="none";
}

//for decrypting
function de_compose(data){
  const de_cryptor = {'a':'2','b':'3','j':'4','w':'5','l':'6','f':'9','m':'8','x':'7','&':'1','x':'0'};
  let value = '';
  for (let i=0;i<data.length;i++){
    value += de_cryptor[data[i]];
  }
  document.getElementById('test').innerHTML = JSON.stringify(value)
  return value;
}

//auto logout
$(document).ready(function(){         
  $(window).on("beforeunload", function(e) {
      $.ajax({
              url: logout_user,
              method: 'GET',
          })
  });
});