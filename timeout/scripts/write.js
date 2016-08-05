$("#sbm").click(checkEmpty);

function checkEmpty(event){
  if(!$.trim($("#inp").val())){
    event.preventDefault();
    alert("Please type in text!");
  }
}
