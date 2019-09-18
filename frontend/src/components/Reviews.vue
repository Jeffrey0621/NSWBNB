<template>
    <div style="border: #ececec 1px solid;width: 100%;margin: 0 12px;">
      <!--title2-->
      <div style="background-color: #ececec;height: 45px;width: 100%;text-align: left">
        <h2 style="padding: 6px 12px 0 12px;color: #484848">Past Reviews about You</h2>
      </div>
      <div style="text-align: left;margin-bottom: 20px">
        <a-list
          class="comment-list"
          itemLayout="horizontal"
          :dataSource="data"
          :pagination="pagination"
        >
          <a-list-item slot="renderItem" slot-scope="item, index">
            <a-comment
              :author="item.author"
              :avatar="item.avatar"
            >
              <template slot="actions">
                <span v-for="action in item.actions">{{action}}</span>
              </template>
              <p slot="content">{{item.content}}</p>
              <a-tooltip slot="datetime" :title="item.datetime.format('YYYY-MM-DD HH:mm:ss')">
                <span>{{item.datetime.fromNow()}}</span>
              </a-tooltip>
            </a-comment>
          </a-list-item>
        </a-list>
      </div>

      <!--title3-->
      <div style="background-color: #ececec;height: 45px;width: 100%;text-align: left">
        <h2 style="padding: 6px 12px 0 12px;color: #484848">Past Reviews You’ve Written</h2>
      </div>
      <div style="text-align: left;margin-bottom: 20px">
        <a-list
          class="comment-list"
          itemLayout="horizontal"
          :dataSource="data"
          :pagination="pagination"
        >
          <a-list-item slot="renderItem" slot-scope="item, index">
            <a-comment
              :author="item.author"
              :avatar="item.avatar"
            >
              <template slot="actions">
                <span v-for="action in item.actions">{{action}}</span>
              </template>
              <p slot="content">{{item.content}}</p>
              <a-tooltip slot="datetime" :title="item.datetime.format('YYYY-MM-DD HH:mm:ss')">
                <span>{{item.datetime.fromNow()}}</span>
              </a-tooltip>
            </a-comment>
          </a-list-item>
        </a-list>
      </div>

    </div>
</template>

<script>
    import moment from 'moment'
    export default {
        data(){
          return{
            data: [
              {
                actions: ['Reply to'],
                author: 'Han Solo',
                avatar: 'https://zos.alipayobjects.com/rmsportal/ODTLcjxAfvqbxHnVXCYX.png',
                content: 'We supply a series of design principles, practical patterns and high quality design resources (Sketch and Axure), to help people create their product prototypes beautifully and efficiently.',
                datetime: moment().subtract(1, 'days'),
              },
              {
                actions: ['Reply to'],
                author: 'Han Solo',
                avatar: 'https://zos.alipayobjects.com/rmsportal/ODTLcjxAfvqbxHnVXCYX.png',
                content: 'We supply a series of design principles, practical patterns and high quality design resources (Sketch and Axure), to help people create their product prototypes beautifully and efficiently.',
                datetime: moment().subtract(2, 'days'),
              },
            ],
            moment,
            pagination:{
              pageSize:1,
              showTotal:total => 'Total '+total+ ' reviews.'
            },
          }
        }
    }
</script>

<style scoped>

</style>
