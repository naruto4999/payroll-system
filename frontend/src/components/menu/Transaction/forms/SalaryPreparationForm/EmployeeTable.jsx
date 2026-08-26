import React from 'react';
import DataGrid from '../../../../UI/DataGrid';

const EmployeeTable = React.memo(({ table, tbodyRef, handleKeyDown, onRowClick, focusedRowRef }) => {
    return (
        <DataGrid
            table={table}
            tbodyRef={tbodyRef}
            getRowId={(row) => row.original.id}
            selectedRowId={focusedRowRef.current}
            selectedIndicatorColumnId="paycode"
            onRowClick={onRowClick}
            onRowKeyDown={handleKeyDown}
            maxHeightClassName="max-h-[80dvh] lg:max-h-[70dvh]"
            tableClassName="table-fixed"
        />
    );
});

export default EmployeeTable;
