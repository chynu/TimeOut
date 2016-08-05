$("#sbm").click(checkEmpty);

function checkEmpty(event){
  if(!$.trim($("#inp").val())){
    event.preventDefault();
    alert("Please type in a kind message for people to read. :)");
  }
}
