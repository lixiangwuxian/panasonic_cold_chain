#include "excel.h"

Excel::Excel()
{
}

bool Excel::SetExcelPath(){
    OPENFILENAME openFileName={};
    char fileName[MAX_PATH]={};
    ZeroMemory(&openFileName,sizeof(openFileName));
    const wchar_t* filter = L"表格文件 (*.xlsx,*.xls)\0*.xlsx;*.xls\0";
    HWND owner = NULL;
    openFileName.lStructSize = sizeof(OPENFILENAME);
    openFileName.hwndOwner = owner;
    openFileName.lpstrFilter = (LPWSTR)filter;
    openFileName.lpstrFile = (LPWSTR)fileName;
    openFileName.nMaxFile = MAX_PATH;
    openFileName.Flags = OFN_EXPLORER | OFN_FILEMUSTEXIST | OFN_HIDEREADONLY;
    openFileName.lpstrDefExt = (LPWSTR)"";
    if(!GetOpenFileName(&openFileName)){
        return false;
    }
    //if(!this->excelBook.loadSheet(fileName,1)){
    //    return false;
    //}
}
