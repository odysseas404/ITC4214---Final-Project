// This script handles the toggle functionality for the filter panel on the catalogue page. When the filter toggle button is clicked, it adds or removes the "filter-panel-open" class to the filter panel, which controls its visibility.

const filterToggleButton = document.querySelector(".filter-toggle-button");

// Select the filter panel element

const filterPanel = document.querySelector(".filter-panel");

// Check if both the filter toggle button and filter panel exist before adding the event listener

if (filterToggleButton && filterPanel) {
    // Add a click event listener to the filter toggle button

    filterToggleButton.addEventListener("click", function () {
        // Toggle the "filter-panel-open" class on the filter panel to show or hide it
        
        filterPanel.classList.toggle("filter-panel-open");
    });
}