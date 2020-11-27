define(['dep','jquery', 'bootstrap', 'amd'], function(d,$,b,m) {
    alert("Load after dependencies");
    $('body').html('JQUERY LOADED AS DEPENDENCY');
    console.log($.fn.jquery);   // Get jquery version
    console.log($.fn.tooltip.Constructor.VERSION);  // Get bootstrap version
    // Call asynch method
    m.alert();
})