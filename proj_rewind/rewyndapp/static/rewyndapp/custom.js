//var myVar = setInterval(myTimer, 1000);
var slider = $("#timeslider");
var start_time = $("#clock1");
var remain_time = $("#clock2");
start_time.innerHTML = slider.value; // display default slider value

// Update the clock values when you you drag the slider handle
slider.oninput = () => {
  start_time.innerHTML = this.value;
}
