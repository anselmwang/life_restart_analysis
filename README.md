我很喜欢前段时间流行的人生重开模拟器。世界很大，有无数我未曾见过的人生。所有的可能空间，在我出生的一瞬间就塌缩的极小，并随着时钟变得越来越小。我很想有机会看见那些未曾成为现实的可能性，与最灿烂的那些可能相比，最卑微的那些同样打动我。如这个简短的故事：“你出生了，是个女孩”、“你从小生活在农村”、“你父母又生了个儿子”、“你的家庭更加困难、吃不饱饭”、“你死了”。

当然，我可以用看书、生活、体验、实践来理解人生的模型，可是这些都太复杂了。只有电子游戏，才敢于给出精确的、简化的模型，毕竟，这只是游戏，何必那么认真呢？毕竟这是一段程序，不精确不简化还怎么写啊？与严肃著作相比，《人生重开模拟器》、《模拟人生》、《文明》等游戏，最无畏、有趣而可贵的地方就在于此了。

说回《人生重开模拟器》，我喜欢他，但我不愿去玩他。因为我实在等不了一次次漫长的、大同小异的随机过程。我自己的生活已经够真实了，在游戏里面为何不能做一回上帝？

所以，为了“从游戏中体验人生“这个可笑的目的，我忍不住看了游戏的源码，又写了一个demo帮助我阅读游戏的核心数据。有兴趣的朋友可以去看看我的demo。

这个游戏给出了什么样的人生模型呢？简单的总结是：
- 大部分人在重复相似的人生，每个年龄自有该发生的事情，时间的洪流将我们卷向未来。
- 到这里为止，我感到：人生而不平等，属性与天赋，是人生的随机数种子。
- 人生的每一年，并不是条件独立的采样过程，而是具有长程依赖关系的随机过程。

下面是更详细的解释。
首先，在每个岁数有一个事件列表，不同的事件有不同的权重。在每个岁数，游戏根据权重随机的选择一个事件。比如在31岁，幸运和不幸都不常见（0.03），平凡而普通才是正常生活

![eents_at_31](https://anselmwang.github.io/assets/images/2021-12-07-life-restart-analysis/2021-12-07-23-41-22.png)

**每一局游戏，同一个年龄，不管是谁，都共享相同的事件列表，这告诉我：大部分人在重复相似的人生，每个年龄自有该发生的事情，时间的洪流将我们卷向未来。**

那么，如何体现个体差异呢？在游戏的开始，每个人有20点，可以分配在不同的属性上，每个人还有不同的天赋。这里简便起见，只介绍属性。可以控制的属性有下面这些：
```
    CHR: "CHR", // 颜值 charm CHR
    INT: "INT", // 智力 intelligence INT
    STR: "STR", // 体质 strength STR
    MNY: "MNY", // 家境 money MNY
```

下面两个属性大家都一样：
```
    LIF: "LIF", // 生命 life LIFE，初始时1
    SPR: "SPR", // 快乐 spirit SPR，初始有值
```
在游戏的过程中，不同的事件会改变属性，而属性又作为事件的前提条件，显式的enable/disable某些事件。如智力太低就很难触发“中考考得很好，上了城里的好高中”这个事件。这是随机的人生中，相对有脉络可循的部分。

**到这里为止，我感到：人生而不平等，属性与天赋，是人生的随机数种子。**

除了属性外，一个事件的发生也会影响未来的事件。下面是我在demo中发现的有趣关系。
比如下图，“你进入流水线工厂工作”的一个前提(观察include)事件是“高考，你考上了专科”，而该事件的前提是：智力<6并且发生过事件”中考考的一般，上了县里的高中”。而当你考上一般高中时，无数的可能性对你关闭了（观察exclude部分），你不会“辍学打工，补贴家用”

![enter_factory](https://anselmwang.github.io/assets/images/2021-12-07-life-restart-analysis/2021-12-07-23-45-57.png)

另一个例子如下，大家自己看看“你成为了世界首富”的可行路径吧。另外，effect_dict里面指出，成为世界首富，会给你增加1点快乐(SPR)。
![be_richest](https://anselmwang.github.io/assets/images/2021-12-07-life-restart-analysis/2021-12-07-23-47-00.png)

**在游戏的人生模型中，人生的每一年，并不是条件独立的采样过程，而是具有长程依赖关系的随机过程。**