require.config({
    baseUrl: 'lib',
    paths: {
        dep: '../app/dependency',
        jquery: [
            'https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min'
            ,'jquery-3.5.1'
        ],
        bootstrap: 'https://cdn.jsdelivr.net/npm/bootstrap@4.5.3/dist/js/bootstrap.bundle.min',
        amd: '../app/amd'
    },
    // shim config
    shim: {
        'bootstrap': {
            // Add jquery as a dependency for bootstrap
            deps: ['jquery']
        }
    }
})

// // Code without Define
// require(['dep','jquery', 'bootstrap'], function() {
//     alert("Load after dependencies");
//     $('body').html('JQUERY LOADED AS DEPENDENCY');
//     console.log($.fn.jquery);   // Get jquery version
//     console.log($.fn.tooltip.Constructor.VERSION);  // Get bootstrap version
// })

// Code with Define
// Note the two dots used for the path. This is needed since we defined the base url as 'lib' and 
// need to traverse to the parent of the 'lib' folder before we can go to the 'app' folder
require(['../app/app'], function() {   
    
})