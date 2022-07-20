#ifndef EXCEL_H
#define EXCEL_H

#include <string>
#include "windows.h"


struct CirculationSheet{
  char* 流转单号;
  char* 生产批号;
  char* 生产台数;
  char* 部品番号;
  char* 定额;
  char* 规格;
  char* 材料;
  char* 保管员;
  char* 安全标识;
  char* 送货量;
  char* 生产线;
  char* 工序;
  char* 接收班组;
  char* 供应商;
  char* 工程名;
  char* 到货日期;
  char* 二维码;
};


class Excel
{
public:
  Excel();
  bool SetExcelPath();
private:
};

#endif // EXCEL_H
