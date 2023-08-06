/*=============================================================================
*     FileName: MekongJS.js
*         Desc: Mekong app SDK
*      Creator: Mekong
*      Version: 1.0.0
*   LastChange: 2023-02-22 16:03:59
*=============================================================================*/
;(function (window, undefined) {
  var UA = navigator.userAgent;
  var isIOS = !!UA.match(/\(i[^;]+;( U;)? CPU.+Mac OS X/i) || !!UA.match(/\(Maci[^;]+; .+Mac OS X/i);
  var isAndroid = !!/Android|Adr/i.test(UA);
  var ApiBridge = {
    msgQueue: [],
    callbackCache: [],
    callbackId: 0,
    processingMsg: false
  };

  ApiBridge.create = function () {
    ApiBridge.bridgeIframe = document.createElement('iframe');
    ApiBridge.bridgeIframe.style.display = 'none';
    document.documentElement.appendChild(ApiBridge.bridgeIframe);
  };

  ApiBridge.getCallbackId = function () {
    return ApiBridge.callbackId++;
  };

  ApiBridge.prepareProcessingMessages = function () {
    ApiBridge.processingMsg = true;
  };

  ApiBridge.fetchMessages = function () {
    if (ApiBridge.msgQueue.length > 0) {
      var messages = JSON.stringify(ApiBridge.msgQueue);
      ApiBridge.msgQueue.length = 0;
      return messages;
    }
    ApiBridge.processingMsg = false;
    return null;
  };

  ApiBridge.onCallback = function (callbackId, obj) {
    if (ApiBridge.callbackCache[callbackId]) {
      ApiBridge.callbackCache[callbackId](obj);
    }
  };

  // TODO event
  ApiBridge.onPushH5 = function (data) {
    MekongJS.emit('onProgress', data);
  };

  ApiBridge.callNative = function (clz, method, args, callback) {
    var msgJson = {};

    msgJson.clz = clz;
    msgJson.method = method;

    if (args != undefined) {
      msgJson.args = args;
    }

    if (callback) {
      var callbackId = ApiBridge.getCallbackId();

      ApiBridge.callbackCache[callbackId] = callback;

      console.log(msgJson);

      if (msgJson.args) {
        msgJson.args.callbackId = callbackId.toString();
      } else {
        msgJson.args = {
          callbackId: callbackId.toString()
        };
      }
    }

    if (window.jsBridgeChannelApi) {
      window.jsBridgeChannelApi.postMessage(JSON.stringify(msgJson));
    }
  };

  /**
   * 接口通用传参回调中转
   * @params { string|Object } clz, 参数对象{ clz: <string|桥接名称|jsBridgeClient,event,ApiBridge>, method: <string|方法名称>, args: <object|参数对象>, callback: <function|回调方法> }
   * @params { string } method
   * @params { Object } args, 参数对象, 默认为{}
   * @params { function } callback 回调方法
   */
  ApiBridge.invoke = function (clz, method, args, callback) {
    if(Object.prototype.toString.call(clz) === '[object Object]'){
      method = clz.method;
      args = clz.args || {};
      callback = clz.callback || null;
      clz = clz.clz || 'jsBridgeChannelApi';
    } else {
      clz = clz || 'jsBridgeChannelApi';
      args = args || {};
    }

    if (callback) {
      ApiBridge.callNative(clz, method, args, callback);
      return;
    } 

    ApiBridge.callNative(clz, method, args);
    return;
  };

  var MekongJS = {
    eventList: {},
    on: function(event, fn){
      // 如果对象中没有对应的 event 值，也就是说明没有订阅过，就给 event 创建个缓存列表
      // 如有对象中有相应的 event 值，把 fn 添加到对应 event 的缓存列表里
      (MekongJS.eventList[event] || (MekongJS.eventList[event] = [])).push(fn);
      return MekongJS;
    },
    emit: function () {
      // 第一个参数是对应的 event 值，直接用数组的 shift 方法取出
      var event = [].shift.call(arguments);
      var fns =  [];

      if(!MekongJS.eventList[event]){
        return false;
      }

      for(var i = 0; i < MekongJS.eventList[event].length; i++){
        fns.push(MekongJS.eventList[event][i]);
      }

      // 如果缓存列表里没有 fn 就返回 false
      if (!fns || fns.length === 0) {
        return false;
      }

      // 遍历 event 值对应的缓存列表，依次执行 fn
      for(var i = 0; i < fns.length; i++){
        var fn = fns[i];
        fn.apply(MekongJS, arguments);
      }

      return MekongJS;
    },

    /*
     * Execute command
     */
    excuting: function(data, callback) {
      return ApiBridge.invoke({
        method: 'excuting',
        args: {
          data: data
        },
        callback: callback
      });
    },
    /*
     * PickImage
     */
    pickImage: function(callback) {
      return ApiBridge.invoke({
        method: 'uploadReportImage',
        callback: callback
      });
    }
  };

  window.ApiBridge = ApiBridge;
  window.MekongJS = MekongJS;
})(window);
