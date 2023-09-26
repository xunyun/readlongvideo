<template>
  <div>

    <div class="container">
    <h1>阅读视频</h1>
    
    <div class="flex-container common-width">
      <t-input v-model="videourl" @keyup.enter.native="handleAction" ></t-input>
      <t-button @click="submitVideoUrl" v-if="!isSubmitting && progress === 0">确定</t-button>
      <t-button @click="submitVideoUrl" loading v-else >确定</t-button>
    </div>
    <p></p>
    <div class="common-width" >
      <t-progress v-if="progress > 0 && !showNotification"  theme="line" :color="{ from: '#0052D9', to: '#00A870' }" :percentage="progress" :status="'active'" />
    </div>
    <div class="dlcontainer">
      <a v-if="showNotification" :href="downloadLink">🔗文档下载链接</a>
    </div>
  
    <p></p>
    <t-drawer  placement="left"
      :visible.sync="visible" header="转换历史记录" 
      :onConfirm="onClickConfirm" 
      :showOverlay="false" 
      :closeBtn="true">
      <ul class="history-links">
        <li v-for="record in historyRecords" :key="record.title">
          <a :href="record.url">🔗{{ record.title }}</a>
        </li>
      </ul>
    </t-drawer>
   
    </div>

    <footer>
        ©readlongvideo
    </footer>
  </div>


</template>


<script>
import axios from 'axios';
import Vue from 'vue';
import TDesign from 'tdesign-vue';
import { MessagePlugin as Message } from 'tdesign-vue';
import {
  SearchIcon, MailIcon, UserIcon, EllipsisIcon, LettersIIcon,
} from 'tdesign-icons-vue';

Vue.use(TDesign);
export default {
  components: {
    SearchIcon,
    MailIcon,
    UserIcon,
    EllipsisIcon,
  },
  data() {
  return {
    videourl: '',
    downloadLink: null,
    isSubmitting: false,
    style: { margin: '20px 0 10px' },
    progress: 0,
    showNotification: false,  // 新的数据属性
    waitForSignal: false, 
    visible: false,
    historyRecords: [
        { title: '历史记录1', url: 'http://www.baidu.com' },
        { title: '历史记录2', url: 'http://www.sogou.com' },
        { title: '历史记录3', url: 'http://www.qq.com' },
        { title: '历史记录4', url: 'http://www.qq.com' },
        { title: '新增一个5', url: 'http://www.qq.com' },
      ],
    menu1Value: 'item2',
    menu2Value: 'item1',
  };
  },
  methods: {
    changeHandler(active) {
      console.log('change', active);
    },
    handleClick() {
      this.visible = true;
    },
    onClickConfirm() {
      Message.info('数据保存中...', 1000);
      const timer = setTimeout(() => {
        clearTimeout(timer);
        this.visible = false;
        Message.info('数据保存成功!');
      }, 1000);
    },
    handleAction() {
      if (!this.isSubmitting && this.progress === 0) {
        this.submitVideoUrl();
      }
      // 这里可以加入更多的逻辑，比如按钮处于loading状态时的处理等。
    },
    submitVideoUrl() {
      if(!this.videourl) {
        alert('请输入URL');
        return;
      }
      this.isSubmitting = true; // 开始提交
      // 在成功收到后端响应后，我们开始显示和更新进度条
      this.updateProgress();

      axios.post('http://localhost:8000/your-backend-endpoint', {
        videourl: this.videourl
      })
      .then(response => {
        this.isSubmitting = false; // 提交完成
        if (response.data.status === 'success') {
          alert('视频URL提交成功！');
          // 假设后端在成功的响应中返回一个downloadLink字段，我们可以这样更新Vue组件中的数据属性
          this.downloadLink = response.data.downloadLink;  // 更新下载链接
          alert(this.downloadLink);
        } else {
          alert('服务器返回了一个错误。');
        }
      })
      .catch(error => {
        this.isSubmitting = false; // 提交完成
        console.error('发送数据时出错:', error);
        alert('发送URL时出错，请稍后再试。');
      });
    },
    updateProgress() {
        if (this.progress < 40) {
            this.progress += 1; 
            this.showNotification = false;
            setTimeout(this.updateProgress, 250);
        } 
        else if (this.progress < 80 ) {
            this.progress += 1; 
            this.showNotification = false;
            setTimeout(this.updateProgress, 500);
            if (this.progress > 50) {
              this.checkDownloadLink();
            }
        }
        else if (this.progress < 95 ) {
            this.progress += 1; 
            this.showNotification = false;
            setTimeout(this.updateProgress, 1000);
            this.checkDownloadLink();
        } 
        else if (this.progress === 95) {
            
            setTimeout(this.updateProgress, 1000);
            this.checkDownloadLink()
        }

        // 在每次进度更新后检查waitForSignal
        if (this.progress >= 51 && this.waitForSignal) {
            this.progress = 100;
            this.isSubmitting = false;
            this.showNotification = true;
            return; // 为了确保不再进行其他操作，直接返回
        }
    },
    checkDownloadLink() {
        fetch(this.downloadLink, {
            method: 'HEAD' // 使用HEAD请求只获取响应头，不下载整个内容
        })
        .then(response => {
            if (response.status !== 404) {
                this.waitForSignal = true;
            }
        })
        .catch(error => {
            console.error('Error checking download link:', error);
        });
    },
    // 当外部信号到达时调用此方法
    onSignalReceived() {
            this.waitForSignal = true;
            // 如果当前进度为95，则直接更新进度到100
            if (this.progress < 95) {
                this.updateProgress();
            }
    }
  }
}

</script>

<style scoped>
h1 {
  color: rgb(7, 7, 123);
}

body {
  margin: 0;  /* 移除默认的 margin */
  padding: 0; /* 如果需要 */
}
.container {
    max-width: 600px;
    margin: 0 auto;
    height: 78vh;
    padding: 20px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    border-radius: 8px;
    font-family: 'Consolas', monospace;
    
}

.page-wrap {
  display: flex;
  flex-direction: column;
  min-height: 100vh; /* 确保至少与视口一样高 */
}

.flex-container {
    display: flex;
    align-items: center; 
}
.search-section {
    display: flex;
    gap: 10px;
    margin: 20px 0;
}
.dlcontainer {
    text-align: center;
}

div > .t-progress-domo-margin:first-child {
  margin-top: 0;
}

.t-progress-domo-margin {
  margin: 16px 0 4px;
}

.common-width {
    width: 100%; /* 或其他你想要的宽度 */
    margin: 0 auto; /* 可选，如果你想要将元素居中 */
  }

.history-links {
  list-style-type: none;
  padding: 0;
}

.history-links li {
  margin-bottom: 10px;
}

.t-menu__operations {
  .t-button {
    margin-left: 8px;
  }
}
.t-demo-menu--dark {
  background-color: #333; /* 深灰色 */
  .t-button {
    color: #fff;

    &:hover {
      background-color: #4b4b4b;
      border-color: transparent;
      --ripple-color: #383838;
    }
  }
}


footer {
            padding: 10px 0;
            text-align: center;
            background-color: #f9f9f9;
            border-top: 1px solid #e1e1e1;
            font-size: 0.9em;
            font-family: 'Consolas', monospace;
}


</style>
