define(['jquery', 'bootstrap', 'bootstrapSelect'], function($) {
    $('select').selectpicker();
	var app = qlik.openApp(appId, config)
	console.log("in nav js :", app)
})