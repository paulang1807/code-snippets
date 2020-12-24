define([], function() {
   
    // Create Bookmark
    $(".bmCreate").click(function(){
        var title = $('#bmTitle').val()
        var desc = $('#bmDesc').val()

        // Create Bookmark
        app.bookmark.create(title, desc)
        $('#bmTitle').val('')
        $('#bmDesc').val('')

        // Hide Form
        $("#form-modal").toggle(false)
    })

    // Display Bookmarks
    app.getList("BookmarkList", function(reply){
        reply.qBookmarkList.qItems.forEach(function(value) {
            $(".bm-list").append('<li class="bm-list-item"> <a class="bm-item-id" data-id="'
            + value.qInfo.qId + '">'
            + '<span class="bm-item-title">' + value.qData.title + '</span>'
            + '<span class="bm-item-desc">' + value.qData.description + '</span></a>'
            // Add option to delete bookmark
            + '<i class="fas fa-trash-alt bm_rmv" data-id="' + value.qInfo.qId + '"></i></li>')

        });

        $(".bm-item-id").click(function(){
            bmId = $(this).data("id")
            // Apply Bookmark
            app.bookmark.apply(bmId)
            // Hide Modal
            $("#bookmarkModal").modal('hide')    // Syntax from bootstrap modal
        })
        $(".bm_rmv").click(function(){
            bmId = $(this).data("id")
            // Remove Bookmark
            app.bookmark.remove(bmId)
            // Hide Modal
            $("#bookmarkModal").modal('hide')
        })
    })
    
});