var config = {
    host: 'qliksensestg.a.intuit.net',    // can use window.location.hostname on the server
    port: 443,    // can use window.location.port on the server
    isSecure: true ,   //use window.location.protocol === "https:" on the server
    prefix: ''
}

var appRequire = require.config({
    context: 'appRequire',
    baseUrl: './',
    paths: {
        jquery: 'https://code.jquery.com/jquery-3.3.1.slim.min',
        bootstrap: 'https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.bundle.min',
        bootstrapSelect: 'https://cdnjs.cloudflare.com/ajax/libs/bootstrap-select/1.13.1/js/bootstrap-select.min'
    },
    shim: {
        'bootstrap': {
            deps: ['jquery']
        },
        'bootstrapSelect': {
            deps: ['jquery', 'bootstrap']
        }
    }
})

var appId = '0655bfca-73e7-43f0-b7b7-8c76164acb05';

// Require config for capability api
require.config({
    baseUrl: (config.isSecure ? 'https://' : 'http://') + config.host + (config.port ? ':' + config.port : '') + '/resources/'
})

// The require parameter below refers to the root of the capability api available in the server
// in https://qliksensestg.a.intuit.net/resources/js/qlik.js
require(['js/qlik'],function(qlik){
    // On error pop up from mashup documentation
	qlik.on( "error", function ( error ) {
		$( '#popupText' ).append( error.message + "<br>" );
		$( '#popup' ).fadeIn( 1000 );
	} );
	$( "#closePopup" ).click( function () {
		$( '#popup' ).hide();
    } );

    // Open temporary app
    var app = qlik.openApp(appId, config)
    // Exporting qlik to have global scope
    window.qlik = qlik
    
    // Require app.js
    require({context: 'appRequire'}, ['./app'])

	//callback functions
    function listCallback(reply, app){   // Here 'reply' will contain the list object
        $(".list1").empty()
        var data = reply.qListObject.qDataPages[0]
        $.each(data.qMatrix, function(key, value){
            var item =  value[0];
            // Add inline style to items to show if it is selected
            var selectStyle = ''
            item.qState == "S" ? (selectStyle = ' style="background-color:green;"') : (selectStyle = ' style="background-color:white;"')
            $(".list1").append('<li ' + selectStyle + '>' + item.qText + '</li>')
        })
        // Add event listener for list item click
        $(".list1 li").click(function(){
            var selection = $(this).text()
            app.field("Dim2").selectValues([selection],true, true)
            // app.getList("SelectionObject", function(){
            //     console.log(selection, " selected")
            // })
        })
    }

	//create cubes and lists 
	app.createList({
		"qFrequencyMode": "V",
		"qDef": {
				"qFieldDefs": [
						"Dim2"
				]
		},
		"qExpressions": [],
		"qInitialDataFetch": [
				{
						"qHeight": 20,   // 20 Rows
						"qWidth": 1      // 1 Column
				}
		],
		"qLibraryId": null
	},listCallback);      // Create list and store it in 'listCallback'
})