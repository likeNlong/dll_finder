

# DLL_Finder 白加黑_DLL挖掘辅助工具



微信公众号：小惜渗透，欢迎大佬一起交流进步，回复`彩蛋`有惊喜

![image-20220819133337175](https://mc-imgup.oss-cn-beijing.aliyuncs.com/202208191333189.png)



* 静默运行，不影响正常计算机使用，不过还是推荐虚拟机内运行
* 目前只针对挖掘`未找到的DLL`



**使用说明：**



1. 先通过Process Monitor按如下过滤器规则，筛选出对应进程`未找到的DLL`的信息

<img src="https://mc-imgup.oss-cn-beijing.aliyuncs.com/202404121601235.png" alt="image-20240412160100152" style="zoom:50%;" />

2. 点击第一条，然后按住shift选择最后一条，达到全选



<img src="https://mc-imgup.oss-cn-beijing.aliyuncs.com/202404121603623.png" alt="image-20240412160310493" style="zoom:50%;" />

3. 右上角编辑复制，粘贴到项目下的dll_name.txt

![image-20240412160402393](https://mc-imgup.oss-cn-beijing.aliyuncs.com/202404121604440.png)

<img src="https://mc-imgup.oss-cn-beijing.aliyuncs.com/202404121604489.png" alt="image-20240412160447401" style="zoom:50%;" />



4. 改好config里面的配置运行即可（未避免权限错误，建议以管理员运行）

<img src="https://mc-imgup.oss-cn-beijing.aliyuncs.com/202404121605939.png" alt="image-20240412160517875" style="zoom:50%;" />



<img src="https://mc-imgup.oss-cn-beijing.aliyuncs.com/202404121615922.png" alt="image-20240412161559856" style="zoom:50%;" />









> 发布白加黑文章后发现已知的DLL挖掘工具都不太好用，于是想自己写一个，初步用了两天时间，存在一些想克服的点，还有一些问题还没解决因时间精力有限后续有空了看看是否更新，或者有大佬有解决方案的话提供一下，我更新到代码中。
>
> * Kill程序后托盘图标问题（已经解决）
> * 遍历到某个DLL时启动EXE，会弹出（进程名为csrss.exe）的系统报错，这个一直没解决，双击运行白程序程序或cmd下python运行脚本启动白程序都报错，但是用pycharm启动脚本就不会弹出系统报错提示，这块应该是一个突破点，但是试了很多还是没解决



