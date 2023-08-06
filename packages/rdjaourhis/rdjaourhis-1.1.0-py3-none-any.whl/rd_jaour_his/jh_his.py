import pandas as pd
from pyrda.dbms.rds import RdClient


def do_his(input_excel, sheet_index, jh_token):

    jh_app = RdClient(token=jh_token)

    df = pd.read_excel(input_excel, sheet_index)
    fbillnumber_DC_I_DRAFTGRADE_df = df[['票据号', '汇票等级']]

    for DC_I_DRAFTGRADE, fbillnumber_df in fbillnumber_DC_I_DRAFTGRADE_df.groupby('汇票等级'):

        DC_I_DRAFTGRADE = str(int(DC_I_DRAFTGRADE))
        fbillnumber_list = fbillnumber_df['票据号'].tolist()
        # print(fbillnumber_list)

        fbillnumbers = '('
        for fbillnumber in fbillnumber_list:
            fbillnumbers = fbillnumbers + f"'{str(int(fbillnumber))}'" + ','
        fbillnumbers = fbillnumbers[:-1] + ')'

        # print(fbillnumbers)

        sql = f"""
                -- select * from T_CN_BILLRECEIVABLE
    
                update T_CN_BILLRECEIVABLE set DC_I_DRAFTGRADE = {DC_I_DRAFTGRADE}
    
                where fbillnumber in {fbillnumbers}
                """
        # print(sql)
        # res = jh_app.select(sql)
        # print(res)

        jh_app.update(sql)


if __name__ == '__main__':
    jh_test_token = 'F91CF3E3-8962-47F2-823F-C5CCAAFC66CA'
    input_excel = r"D:\RDS\jh\需处理历史单据清单.xlsx"
    sheet_index = 1
    do_his(input_excel, sheet_index, jh_test_token)