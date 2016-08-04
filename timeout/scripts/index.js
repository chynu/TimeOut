var quest = $("#quest");
var popup = $(".popup");
var clicked = false;

quest.click(function(){
  if (clicked){ popup.fadeOut(300); }
  else { popup.fadeIn(300); }
  clicked = !clicked;
});
