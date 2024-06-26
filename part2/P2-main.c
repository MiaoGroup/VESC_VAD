/*
 * Copyright (c) 2024, VeriSilicon Holdings Co., Ltd. All rights reserved
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are met:
 *
 * 1. Redistributions of source code must retain the above copyright notice,
 * this list of conditions and the following disclaimer.
 *
 * 2. Redistributions in binary form must reproduce the above copyright notice,
 * this list of conditions and the following disclaimer in the documentation
 * and/or other materials provided with the distribution.
 *
 * 3. Neither the name of the copyright holder nor the names of its contributors
 * may be used to endorse or promote products derived from this software without
 * specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
 * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
 * DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
 * FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
 * DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
 * SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
 * CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
 * OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
 * OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 */

#include <stdint.h>
#include "vs_conf.h"
#include "soc_init.h"
#include "soc_sysctl.h"
#include "bsp.h"
#include "uart_printf.h"
#include "board.h"
#include "osal_task_api.h"
#include "vpi_error.h"
#include "vpi_event.h"
#include "main.h"

static int sys_manager_handler(void *cobj, uint32_t event_id, void *param) {
	uart_printf("value: 0x%lx", *(uint32_t*) param);
	return 0;
}

static void task_sys_mgr(void *param) {
	void *pSysManager = vpi_event_new_manager(COBJ_SYS_MGR,
			sys_manager_handler);
	vpi_event_register(EVENT_SYS_TEST, pSysManager);

	while (1) {
		vpi_event_listen(pSysManager);
	}

}

static int custom_manager_handler(void *cobj, uint32_t event_id, void *param) {
	return 0;
}

static void task_custom_mgr(void *param) {
	void *pCustomManager = vpi_event_new_manager(COBJ_CUSTOM_MGR,
			custom_manager_handler);
	(void) pCustomManager;

	uint32_t v = 0xa5a5;
	osal_sleep(1000);
	vpi_event_notify(EVENT_SYS_TEST, &v);

	osal_sleep(INT32_MAX);

}

static void task_init_app(void *param) {
	BoardDevice board_dev;

	/* Initialize board */
	board_register(board_get_ops());
	board_init((void*) &board_dev);
	if (board_dev.name)
		uart_printf("Board: %s", board_dev.name);

	uart_printf("Hello VeriHealthi!\r\n");

//	osal_create_task(task_sample, "task_sample", 512, 4, NULL);
	osal_create_task(task_sys_mgr, "task_sys_mgr", 512, 4, NULL);
	osal_create_task(task_custom_mgr, "task_custom_mgr", 512, 4, NULL);
	osal_delete_task(NULL);
}

int main(void) {
	int ret;

	ret = soc_init();
	ret = vsd_to_vpi(ret);
	if (ret != VPI_SUCCESS) {
		if (ret == VPI_ERR_LICENSE)
			uart_printf("no sdk license!");
		else
			uart_printf("soc init error");
		goto exit;
	} else {
		uart_printf("soc init done");
	}

	osal_create_task(task_init_app, "init_app", 512, 1, NULL);
	osal_start_scheduler();

	exit: while (1)
		;
	return 0;
}
