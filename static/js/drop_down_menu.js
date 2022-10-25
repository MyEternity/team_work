   $(document).ready(function() {
      // Listener for when you click on the dropdown menu
      $('.toggle-item > .legend-container').on('click', (event) => {
        // Adds or removes the 'selected' attribute on the dropdown menu you clicked
        $(event.currentTarget).parent().toggleClass('selected')
        // If you have multiple dropdown menus you may want it so that when you open Menu B, Menu A
        // automatically closes.
        // This line does that by removing 'selected' from every dropdown menu other than the one you clicked on.
        // It's 'optional' but it definitely feels better if you have it
        $('.toggle-item').not($(event.currentTarget).parent()).removeClass('selected')
      })

      // The user is probably going to expect that any and all dropdown menus will close if they click outside of them. Here's how to make that happen:

      //This listens for whenever you let go of the mouse
      $(document).mouseup(function(e)
          {
              // make this a variable just to make the next line a little easier to read
              // a 'container' is now any
              var dropdown_menus = $(".toggle-item");

              // if the target of the click isn't a dropdown menu OR any of the elements inside one of them
              if (!dropdown_menus.is(e.target) && dropdown_menus.has(e.target).length === 0)
              {
                // then it will de-select (thereby closing) all the dropdown menus on the page
                  $('.toggle-item').removeClass('selected')

              }
          });
    })