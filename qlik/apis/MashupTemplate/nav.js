define(['jquery', 'bootstrap', 'bootstrapSelect'], function($) {
	$('select').selectpicker();

	// Hide new bookmark form on load
	$("#form-modal").toggle(false)

	// Show bookmark form on clicking 'New'
	$(".bmNew").click(function(){
		$("#form-modal").toggle(true)
		$(".bmCreate").prop("disabled", false)
		$(".bmNew").prop("disabled", true)
	})

	// Update bookmark on modal close
	$("#bookmarkModal").on("hidden.bs.modal", function(){
		$("#form-modal").toggle(false)
		$(".bmCreate").prop("disabled", true)
		$(".bmNew").prop("disabled", false)
	})

	// Undo, Redo and Clear
    $('[data-control]').click(function(){
        var element = $(this)
        switch(element.data('control')) {
            case 'back': 
                app.back()
            break;
            case 'forward': 
                app.forward()
            break;
            case 'clear': 
                app.clearAll()
            break;
        }
    })
})