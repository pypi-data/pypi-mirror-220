/*! © Lokesh Babu - datatables.net/license */

(function( factory ){
	if ( typeof define === 'function' && define.amd ) {
		// AMD
		define( ['jquery', 'datatables.net'], function ( $ ) {
			return factory( $, window, document );
		} );
	}
	else if ( typeof exports === 'object' ) {
		// CommonJS
		var jq = require('jquery');
		var cjsRequires = function (root, $) {
			if ( ! $.fn.dataTable ) {
				require('datatables.net')(root, $);
			}
		};

		if (typeof window !== 'undefined') {
			module.exports = function (root, $) {
				if ( ! root ) {
					// CommonJS environments without a window global must pass a
					// root. This will give an error otherwise
					root = window;
				}

				if ( ! $ ) {
					$ = jq( root );
				}

				cjsRequires( root, $ );
				return factory( $, root, root.document );
			};
		}
		else {
			cjsRequires( window, jq );
			module.exports = factory( jq, window, window.document );
		}
	}
	else {
		// Browser
		factory( jQuery, window, document );
	}
}(function( $, window, document, undefined ) {
'use strict';
var DataTable = $.fn.dataTable;


DataTable.render.hyperLink = function (anchorText, location, width, height) {
    var validateAndReturnDefaultIfFailed = function (item, defaultValue) {
        if (typeof item === 'number') {
            return item;
        }
        if (typeof item === 'string') {
            return parseInt(item) ? item : defaultValue;
        }
        return defaultValue;
    };
    var anchorText = anchorText || 'Click Here';
    var location = location || 'newTab';
    var width = validateAndReturnDefaultIfFailed(width, 600);
    var height = validateAndReturnDefaultIfFailed(height, 400);
    return function (data, type, row) {
        // restriction only for table display rendering
        if (type !== 'display') {
            return data;
        }
        var url = data;
        // try {
            // url = new URL(data);
        switch (location) {
            case 'newTab':
                return ('<a title="' +
                    url +
                    '" href="' +
                    url +
                    '" target="_blank">' +
                    anchorText +
                    '</a>');
            case 'popup':
                return ('<a title="' +
                    url +
                    '" href="' +
                    url +
                    '" target="popup" rel="noopener noreferrer" onclick="window.open(\'' +
                    url +
                    "', '" +
                    anchorText +
                    "', 'width=" +
                    width +
                    ',height=' +
                    height +
                    '\'); return false;">' +
                    anchorText +
                    '</a>');
            default:
                return ('<a title="' +
                    url +
                    '" href="' +
                    url +
                    '">' +
                    anchorText +
                    '</a>');
        }
        // }
        // catch (e) {
            // return url;
        // }
    };
};


return DataTable;
}));