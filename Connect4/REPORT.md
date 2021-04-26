# Connect-Four

### 实验目的

* Realize the Connect 4 Ai and improve it
* Based on the four-men chess game as the background, through the improvement of pruning algorithm and chess game evaluation, the practical application ability of artificial intelligence algorithm is exercised.

### 实验基础

* Minimax search process
     * The minimax search method is the basic method of game tree search. The main idea is to consider the two sides of the game after several steps (that is, to solve within a limited search depth), choose the relatively best one from the possible steps .
     * To this end, a static estimation function F must be defined. The selection of F is equivalent to the player's ability to judge the game. Therefore, the selection of F is a big factor that affects the intelligence of AI.
* α-β search process
     * α-β is an important pruning optimization for the minimax search process.
     * α(β) Pruning: If the β(α) value of any minimum (large) value layer node is less than (greater than) or equal to the α(β) value of any of its ancestor nodes with maximum (small) value, then There is no need to perform the search process below the MIN(MAX) node.
### 简单实现

*  First, the preliminary version is implemented based on the minimax search process and α-β pruning optimization. The code for the maximum search process is as follows

    ```c++
    int SearchMax(int depth, int alpha, int beta) {	//	DFS
        if (depth >= maxDepth) return F(2) - F(1);	//	超出深度限制
        int maxval = -INF * INF;
        for (int y = 0; y < n; y++) {
            int &&x = Top(y);	if (x == -1) continue; 	//	如果当前列已满
                myboard[x][y] = 2;
                if (machineWin(x, y, m, n, myboard)) {
                  	//	若落子后赢了，则返回∞，同时应该取步数小的，可以乘一个系数
                    myboard[x][y] = 0;
                    return INF * (1 + maxDepth - depth);
                }
                int &&val = SearchMin(depth + 1, max(alpha, maxval), beta);
                myboard[x][y] = 0;	//	回溯
                if (val > maxval) {
                    maxval = val;
                    if (maxval >= beta) return maxval;       //	β 剪枝
                }}}
        return maxval;}
    ```

* The design of the position evaluation function F

     * Consider the number of two-links and three-links, and multiply them by the corresponding weights. This can promote one's own AI to connect into more links, and at the same time tend to interrupt the opponent's links, and is "long" To achieve an optimal balance between “multiple” and “multiple” through the selection of parameters. It is a basic approach.

* The implementation of the preliminary version is completed. After testing, it is found that the search depth is 4 without overtime, that is, it is speculated that each party will take 2 steps and play against 100. The winning rate is about 30%.

### 简单优化

* When you start a few steps, you should try to fall in the middle instead of on both sides.
* The optimization of the evaluation function. First of all, the two ends are not the opponent's pawns and are not forbidden. Such ties are meaningful, so this judgment is increased.
* Considering that the winning strategies are different, only the strategy with fewer steps and the winning strategy should be regarded as the winning strategy. Otherwise, to give a negative extreme example, if the winning strategy with the most steps is taken each time, Eventually, it may fail due to the inaccuracy of the evaluation function.
* As the depth increases, α-β pruning can be more flexible, such as pruning close to the pruning condition, but because the chessboard is too small and the depth is not deep, the effect of pruning is not great, so this pruning is not used.

### 进一步优化

* Evaluation function F optimization
    * During the debugging process, it was found through the output of the chessboard information that the shape of the "concave" glyph often appeared. This was caused by the fact that one side placed a piece and the other side placed another piece to win. The only way to break this deadlock is to wait until there is no other place to play.
    * Therefore, pay attention to the judgment that the two ends are empty in the evaluation function. As the game progresses, the "groove" of a deadlock will become deeper and deeper. Obviously, the pieces on both sides of the groove should not be regarded as valid for one side empty. The pawns should be regarded as blocked pawns. Therefore, this judgment condition is added, that is, the empty position next to it should not be too far from the bottom. Such an empty position is beneficial to the situation.
    * The optimization is believed to be effective after testing.
* Time control optimization
    * There is a time limit of 3s for single-step decision-making. Debugging found that if a fixed search depth is set and forced to return when the time limit is approaching, the accumulation of errors caused by this strategy may be fatal, because it loses a lot of search breadth. For example: the search space in a certain column is very large, and almost all the time is spent in this branch. However, this is no different from directly under this column without searching.
    * The breadth of the search must be fully guaranteed, and if the time is evenly distributed, because certain columns must be defeated within a few steps, this will cause a lot of waste.
    *Adopt adaptive depth, that is, if the time used in the search process reaches half of the time limit, the depth will be limited to -1; if the time used after the entire search is too short, the depth will be limited by +1 to make full use of the time next time.
    * After such negative feedback, the search breadth is guaranteed, and the actual use time is stable within an acceptable range.
    * The optimization is considered to be very effective after experimentation.
    * Considering that the call constant of clock() is relatively large, it is not judged every time.
* Exploratory search optimization
    * Due to the characteristics of the use of α-β pruning, an optimization scheme is thought of: If you first search for the position where the optimal solution may be generated to produce a relatively good solution, it should be possible to prun the subsequent search to the greatest extent! !
    * Therefore, first set the search depth to 3, perform a tentative search, sort by this result, and then perform the original search.
    * Due to the above time control optimization, it is equivalent to automatically deepening the search depth while pruning, and theoretically better results will be obtained.
    * After experimentation, the optimization is considered to be very effective.


### α-β 剪枝 实验效果

*   Use Compete to test 2-100.dylib. According to the scoring rules, you will get 80~90 points.



### 蒙特卡洛树搜索（最终提交）

*   Since the overall effect of the above optimization of α-β pruning was not outstanding, it happened that DDL was postponed, so I decided to write another Monte Carlo tree search.

### 实验基础

*   蒙特卡洛规划
*   信心上限算法

>   信心上限树算法(UCT)
>
>     function UCTSEARCH(𝑠0)
>       以状态𝑠0创建根节点𝑣0;
>       while 尚未用完计算时长 do:
>         𝑣𝑙 ←TREEPOLICY(𝑣0);
>         ∆←DEFAULTPOLICY(s(𝑣𝑙 ));
>         BACKUP(𝑣𝑙 , ∆);
>       end while
>       return 𝑎(BESTCHILD(𝑣0, 0));
>
>     function TREEPOLICY(𝑣)
>       while 节点𝑣不是终止节点 do:
>         if 节点𝑣是可扩展的 then:
>           return EXPAND(𝑣)
>         else:
>           𝑣 ← BESTCHILD(𝑣, 𝑐)
>       return 𝑣
>
>     function EXPAND(𝑣)
>       选择行动𝑎 ∈ 𝐴(𝑠𝑡𝑎𝑡𝑒(𝑣))中尚未选择过的行动
>       向节点𝑣添加子节点𝑣′，使得𝑠(𝑣′)= 𝑓(𝑠(𝑣), 𝑎), 𝑎(𝑣′) = 𝑎
>       return 𝑣′
>
>     function BESTCHILD(𝑣, 𝑐)
>       return 𝑎𝑟𝑔𝑚𝑎𝑥𝑣′∈𝑐h𝑖𝑙𝑑𝑟𝑒𝑛 𝑜𝑓 𝑣 (𝑄(𝑣′) + 𝑐√2𝑙𝑛(𝑁(𝑣)))
>
>     function DEFAULTPOLICY(𝑠)
>       while 𝑠不是终止状态 do:
>         以等概率选择行动𝑎 ∈ 𝐴(𝑠)
>         𝑠 ← 𝑓(𝑠, 𝑎)
>         return 状态𝑠的收益
>
>     function BACKUP(𝑣, Δ)
>       while 𝑣 ≠ 𝑁𝑈𝐿𝐿 do:
>         𝑁(𝑣) ← 𝑁(𝑣) + 1
>         𝑄(𝑣) ← 𝑄(𝑣) + ∆
>         ∆← −∆
>         𝑣 ← 𝑣的父节点

*   学习了 “蒙特卡洛树搜索.pdf” 讲义中相关的部分，核心为如上引用的算法框架。

### 简单优化

*   In the confidence limit index, the value of the constant C can be selected. After testing and comparison, select C = 0.8

### 进一步优化

* State storage
    * Obviously, it is unreasonable for each node to save the entire chessboard, which will produce a lot of redundancy. Consider that each node only saves the points and players placed, so that the storage space and copy time can be minimized, and a complete chessboard can be obtained through the transfer of state; however, until the leaf node is visited, each move These paths all need to update the chessboard step by step. If the search depth is deeper, it will cause unnecessary waste.
    * Therefore, what I consider is state compression. For each node, store two one-bit u_short arrays of state[], top[], binary in state[], 0 means user, 1 means machine means the state of the board, you can use Bit operation & get the state on the two-dimensional chessboard, use top[] to store the position of the top of the chessboard to distinguish between users and empty positions. In this way, you can use memcpy() to copy. Since the operation is continuous memory and only done once, it is not considered much slower than updating one or two points on the board every time.
    * At the same time, due to the existence of the top[] array, finding the next possible point can be completed in linear time. Since Expand() and DefaultPolicy() need to be used many times to find points, in fact, this improvement is not small. (If you use the method of passing the chessboard, to achieve this optimization, you can also maintain and pass the top[] array in addition)
    * In addition, since the complete state is recorded and compressed, it is more suitable for further optimization-hashing, that is, the simulation of walking to the same chessboard state in different orders should be shared (make full use of Markov ), but due to the complexity of hash backtracking processing, this optimization is not added.
* Expansion plan
    * The use of sequential expansion instead of random expansion does not affect the results.
    * Consider Expand(), that is, a node expansion scheme. Thanks to the existence of the top[] array, finding an expandable child node (that can place a point) only needs linear time about the length and width of the board, in fact it is used Appropriate techniques can be divided into O(1) time: from left to right, find the next point, and then start from the selected point in the previous step.

### 更进一步优化

* Efficient maintenance of search tree
    * In view of the characteristics of the confidence limit algorithm decision-making, the walk with the most simulation times is selected each time, so the connection between steps is often much larger than 1/the width of the chessboard. This should be fully utilized.
    * Therefore, you should not rebuild the tree every time, but use MoveRoot() to "move" the root based on the decision in the previous step, completely retaining the results of the previous simulation here, and saving a lot of time for establishing nodes.
    * At the same time, in order to prevent memory leaks and the nodes that need to be deconstructed are piled up in the last step, the method of destructuring while moving the root is adopted: after finding the child node of the root that needs to be moved, deconstruct the rest of its sibling nodes, and then decompose the root Moving down, the destructuring pressure can be evenly divided into each step.
    * In actual implementation, since the destruction time cannot be controlled, the decision of the previous step can be saved, and the operation of moving root and destructuring can be performed before the next step to fully and safely use the time limit.
* Minimize the cost of useless branches
    * Note that the non-main branches of the search tree often contain certain wins and certain defeats, that is, it is the final state. Due to the requirements of the confidence upper bound algorithm, there will inevitably be simulations reaching them, and when the simulations reach them, Since these nodes cannot be expanded further, they simulate themselves again. At this time, double calculations should be avoided.
    * Further optimization can directly delete these useless final states (in fact, assign a very large value instead of -delta, so that the algorithm completely loses confidence in them, and more visits to more useful nodes), and You can refer to the idea of ​​α-β pruning to optimize more related branches.

### MCTS 实验效果

*   With the above optimization and the 2s time limit, the final win rate against 100.dylib is about 85%-95%, and the total win rate is about 96%.

### 代码框架

-   Since the second method is tried out of interest, the process of writing code pays more attention to decoupling to improve the reusability of the code, and does not pursue optimization constants.

```c++
class BoardState : public MonteCarloSearchState
{
public:
	BoardState(bool player);
    BoardState(const BoardState &predstate, int x, int y);
	virtual ~BoardState();
	std::pair<int, int> GetPutLocation();
    MonteCarloSearchState *NextChildState() override;
    int DefaultPolicy() override;
	void Print() override;
};

class BoardTreeNode : public MonteCarloSearchTreeNode
{
public:
    BoardTreeNode(MonteCarloSearchState *state, MonteCarloSearchTreeNode *parent) : MonteCarloSearchTreeNode(state, parent)
    {}
    MonteCarloSearchTreeNode *Expand() override;
};

class BoardTree : public MonteCarloSearchTree
{
	float UCB1(MonteCarloSearchTreeNode *parent, MonteCarloSearchTreeNode *child);
	MonteCarloSearchTreeNode *BestChild(MonteCarloSearchTreeNode *parent);
	void BackTrace(MonteCarloSearchTreeNode *node, int value);
public:
	static time_t StartTime;
    BoardTree(bool player) : MonteCarloSearchTree(new BoardTreeNode(new BoardState(player), nullptr))
    {}
    MonteCarloSearchTreeNode *TreePolicy() override;
	void MoveRoot(std::pair<int, int> put);
	std::pair<int, int> MonteCarloTreeSearch();
};
```
