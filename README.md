# 5_bits_image
# 算法原理：
    这个项目呢是一种格式
    这种格式可以帮你保存基于24位或者32位色深的图片
    但是呢他的每一个单颜色仅五bits构成
    就是怎么做到的呢？让我们来展示一下它的原理
    就像这样00000 11111 11110 11100 00000，就表示31，30，28
    也许你已经猜出来了原理，周围用零包括起来。意味着他们的偏移值是零，
    然后中间的值加上偏移值乘32。嗯，就是实际表现的。
    没错这种压缩算法在有大面积的相近颜色是非常好用的，因为呢相近颜色我们就可以把它们只用五个bit来表示
    那假如我们要表示32怎么办？也许你也已经猜出来了。就是这样表示：00001 00001 00001，偏移值为1，中间的值加上偏移值乘32
    好了，这就是他的算法原理。至于具体的实现细节，大家还是看代码
    不过呢目前为止，这个项目只完成了一点点，大家可以期待一下这个项目的完成，也请大家多多支持
    根据我的预想，这种格式最大长宽为18,446,744,073,709,551,615，
    色深目前只支持24位或32位，但后续会做出增加
    而且在后续有可能会加入压缩模式，即让图片变成一个压缩包
# 缘分的穹空 制作
