# eZoo-GNN

---

eZoo-GNN项目，以eZoo DB为数据基础，集成图神经网络（GNN）的相关功能。在统一的GDB数据基础之上，构建一体化的图智能平台。

此文档包含eZoo-GNN产品的架构及模块介绍及基本的集成、使用方法说明。

如果您有任何新的需求与疑问，欢迎[联系我们](./../../联系我们.md)。

---

## 架构简介

![](images/gnn-arch.jpg)

GNN平台架构分成内核及工具链两部分，内核中包含与模型训练、模型推理、数据加载直接相关的底层模块；工具链中包含训练GNN模型所需要工具包。

eZoo-GNN和ezoo-GDB使用统一的数据引擎，通过数据加载器，将图数据从GDB引擎加载到训练内存中为GNN训练做好准备。之后，用户可以使用GNN训练模块提供的底层接口，定义GNN模型并启动训练；使用GNN推理接口进行模型推理工作。

GNN的操作接口以Python语言形式提供，需要使用者对GNN原理及业务都有足够的了解才能编写符合业务需求的模型逻辑。为了进一步简化模型定义和训练工作，我们预置了GCN、GraphSage、GAT等算法，使用者根据实际需求，通过工具链中的模型参数定义模块指定模型训练时所使用的超参数，并通过模型训练工作流模块指定模型的训练、验证和部署。同时，当你希望对节点特征值进行特征工程时，可以使用数据预处理工具包。它支持正则化、标准化、独热编码等通用的特征工程操作，同时，可以利用图特有的能力，将图挖掘（中心度、分群计算等）的结果生成为节点特征。

---

## 目录结构
在项目工程的src/gnn目录中包含了所有eZoo-GNN相关的代码实现，其中主要的目录及功能：	
+ 根目录文件：
    + setup.py：ezoognn的编译打包定义文件
    + build.sh：启动ezoognn的编译过程
    + gen-whl.sh：生成ezoognn的wheel包，供后续安装
    + start_train.py：训练示例启动主入口
+ [ezoognn](ezoognn/README.md)：eZoo-GNN的主要实现类，几个主要的内容：
    + ezoo_graph.py：对底层eZooGraph的Python封装
    + loader目录：数据加载器，用于GNN训练时从底层图库加载数据
    + sampler目录：采样器，进行随机批次训练、随机游走等计算时在eZoo图中进行采样
    + distribution目录：分布式训练相关实现类
    + utils目录：gnn相关工具包，包括图特征工程工具FeatureMaker、模型存取工具、GNN可视化工具等
+ [ezoognnexample](ezoognnexample/README.md)：eZoo-GNN的示例代码
    + jupyternotebook目录：以jupyter notebook形式组织各不同的GNN应用示例
    + loadingwholegraph目录：以全图数据加载方式进行GNN训练的示例
    + stochastic目录：随机批次方式进行GNN训练的示例
    + fullgraph目录：针对预置数据集，展示不同GNN算法的使用方法
+ [机器学习流水线工具（ezoognngo)](ezoognngo/README.md)：根据配置文件指定的参数（模型类型、数据集、模型超参数等）快速生成特征工程代码、训练代码、执行训练任务等。
+ [测试用例（pytestunit）](pytestunit/README.md)：python单元测试用例
+ [cpp](cpp/README.md)：eZoo-GNN的c++接口层实现
+ test：cpp单元测试用例

---

## 编译安装	

+ 编译gnn动态库，使用项目根目录编译gnn target：
    ```shell
    cd <project_workspace>
    mkdir build
    ```
    + Release版本：
    ```shell
    cmake --build ./build --config Release --target gnn --
    ```
    + Debug版本：
    ```shell
    cmake --build ./build --config Debug --target gnn --
    ```
+ 编译Cython部分：
    ```shell
    cd <project_workspace>/src/gnn
    bash ./build.sh
    ```
这之后即可在源代码目录的中执行主入口文件start_train.py等。

+ 生成wheel：
当希望生成whl包并安装到系统环境时，使用如下命令生成whl文件：
    ```shell
    cd <project_workspace>/src/gnn
    bash ./gen_whl.sh
    ```
脚本执行完成后，会在src/gnn目录中生成子目录**ezoo-gnn-whl**，其中放置了ezoo-gnn模块的安装文件，对其进行**pip install**即可将ezoognn安装到系统的Python目录中。

---

## 执行	

项目中有大量GNN示例代码可供执行：

+ 通过Python执行
```shell
cd <project_workspace>/src/gnn
python start_train.py --cfg-file <eZooDB配置文件路径>
```
**start_train.py**中还有很多其它可配置参数，通过**help**参数查看：
```shell
python start_train.py --help
```

+ 通过jupyter notebook执行
安装ezoognn包之后，启动jupyter notebook，在**src/gnn/ezoognnexample/jupyternotebook**中打开需要的ipynb文件，根据说明执行。