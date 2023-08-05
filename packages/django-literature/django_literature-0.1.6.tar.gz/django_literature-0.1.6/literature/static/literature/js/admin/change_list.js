if (!$) {
  $ = django.jQuery;
}

function getIcon( id ) {
  return `
    <svg class="bi" width="16" height="16" fill="currentColor">
      <use xlink:href=" ${iconURL}#${id}"/>
    </svg>
  `
}

$(function () {
  var table = $("#result_list").DataTable( {
    ajax: {
      url: URL,
      dataSrc: 'results'
    },
    columnDefs: [
    { 
      targets: 0, 
      orderable: false,
      className: 'noVis noPrint'
    },
    {
      targets: 1,
      render: DataTable.render.hyperLink( getIcon("edit"), "default" ),
      className: 'noVis noPrint'
    },
    ],
    colReorder: {
      fixedColumnsLeft: 2,
    },
    stateSave: true,
    dom: 'QBfrtip',
    fixedHeader: true,
    lengthMenu: [
      [ 10, 25, 50, -1 ],
      [ '10 rows', '25 rows', '50 rows', 'Show all' ]
    ],
    searchPanes: {
      layout: 'columns-1'
    },
    buttons: [
      'pageLength',
      {
        extend: 'print',
        exportOptions: {
            columns: ':not(.noPrint) :visible'
        }
      },
      {
        extend: 'collection',
        text: 'Export',
        buttons: [ 
          {
            extend: 'csv',
            exportOptions: {
                columns: ':not(.noPrint) :visible'
            }
          },
          {
            extend: 'excel',
            exportOptions: {
                columns: ':not(.noPrint) :visible'
            }
          },
          {
            extend: 'pdfHtml5',
            orientation: 'landscape',
            pageSize: 'LEGAL',
            exportOptions: {
                columns: ':not(.noPrint) :visible'
            }
          },

      ],
      },
      {
        extend: 'searchPanes',
        config: {
            cascadePanes: true
          }
      },
      {
        extend: 'colvis',
        text: 'Columns',
        collectionLayout: 'fixed columns',
        collectionTitle: 'Column visibility control',
        columns: ':not(.noVis)'
    },
    // 'colvisRestore',
    ],

  } );

//   new $.fn.dataTable.Buttons(table, {
//     buttons: [
//       {
//         extend: 'print',
//         exportOptions: {
//             columns: ':not(.noPrint) :visible'
//         }
//       },
//       {
//         extend: 'collection',
//         text: 'Export',
//         buttons: [ 
//           {
//             extend: 'csv',
//             exportOptions: {
//                 columns: ':not(.noPrint) :visible'
//             }
//           },
//           {
//             extend: 'excel',
//             exportOptions: {
//                 columns: ':not(.noPrint) :visible'
//             }
//           },
//           {
//             extend: 'pdf',
//             exportOptions: {
//                 columns: ':not(.noPrint) :visible'
//             }
//           },
//       ],
//       },

//       {
//         extend: 'colvis',
//         text: 'Columns',
//         collectionLayout: 'fixed columns',
//         collectionTitle: 'Column visibility control',
//         columns: ':not(.noVis)'
//     },
//     // 'colvisRestore',
//     ],
// }); 

  // table.buttons().container().appendTo( $('ul.object-tools') );

});