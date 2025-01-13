import Highcharts from 'highcharts/highstock' // Import Highstock, which includes stock chart functionality
import Exporting from 'highcharts/modules/exporting' // Correct import for Exporting
import Accessibility from 'highcharts/modules/accessibility' // Correct import for Accessibility

// Initialize Highcharts modules
if (typeof Exporting === 'function') {
  Exporting(Highcharts) // Initialize Exporting if available
}

if (typeof Accessibility === 'function') {
  Accessibility(Highcharts) // Initialize Accessibility if available
}

export default Highcharts
