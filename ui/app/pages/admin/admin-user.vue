<template>
  <div class="flex min-h-screen bg-[#0c0c0c] text-white font-sans">
    <!-- Sidebar -->
    <aside class="fixed w-56 flex-shrink-0 bg-[#141414] border-r border-[#232323] flex flex-col py-5">
      <div class="flex items-center gap-2.5 px-5 pb-5 border-b border-[#232323] mb-4">
        <div class="w-8 h-8 rounded-full bg-[#c81e2c] flex items-center justify-center text-[9px] font-bold">
          DE
        </div>
        <div class="font-extrabold text-[15px] tracking-wide">DRIVEEASE</div>
      </div>

      <div class="text-[11px] text-[#6b6b6b] uppercase tracking-wide px-5 pt-3.5 pb-2">Main</div>

      <a
        v-for="item in mainNav"
        :key="item.label"
        class="flex items-center justify-between px-5 py-2.5 text-sm cursor-pointer no-underline"
        :class="item.active
          ? 'text-white bg-[#1c1c1c] border-l-[3px] border-[#c81e2c] font-semibold pl-[17px]'
          : 'text-[#a8a8a8]'"
      >
        <span class="flex items-center gap-3">
          <span class="w-4 h-4 flex items-center justify-center opacity-80" v-html="item.icon"></span>
          {{ item.label }}
        </span>
        <span
          v-if="item.badge"
          class="bg-[#c81e2c] text-white text-[11px] font-bold px-[7px] py-[2px] rounded-full"
        >{{ item.badge }}</span>
      </a>

      <div class="text-[11px] text-[#6b6b6b] uppercase tracking-wide px-5 pt-3.5 pb-2">Report</div>

      <a
        v-for="item in reportNav"
        :key="item.label"
        class="flex items-center justify-between px-5 py-2.5 text-sm text-[#a8a8a8] cursor-pointer no-underline"
      >
        <span class="flex items-center gap-3">
          <span class="w-4 h-4 flex items-center justify-center opacity-80" v-html="item.icon"></span>
          {{ item.label }}
        </span>
      </a>
    </aside>

    <!-- Main -->
    <div class="flex-1 flex flex-col">
      <div class="bg-[#0c0c0c] border-b border-[#1f1f1f] px-8 py-[18px] flex justify-between items-start">
        <div>
          <h1 class="text-xl font-extrabold">Admin / Users</h1>
          <div class="text-[#8a8a8a] text-[13px] mt-1">{{ today }}</div>
        </div>
        <div class="flex items-center gap-2 bg-[#1c1c1c] border border-[#2a2a2a] pl-1.5 pr-3 py-1.5 rounded-full text-sm">
          <div class="w-[26px] h-[26px] rounded-full bg-[#c81e2c] flex items-center justify-center">
            <svg viewBox="0 0 24 24" width="14" height="14" stroke="#fff" stroke-width="2" fill="none">
              <circle cx="12" cy="8" r="3.5" /><path d="M5 20c0-4 3.1-6.5 7-6.5s7 2.5 7 6.5" />
            </svg>
          </div>
          Hi, Admin ⌄
        </div>
      </div>

      <div class="px-8 py-7">
        <div class="flex justify-between items-end mb-[22px]">
          <div>
            <h2 class="text-[22px] font-extrabold">Users</h2>
            <div class="text-[#8a8a8a] text-[13px] mt-1">Manage customer and staff accounts</div>
          </div>
          <button class="bg-[#c81e2c] hover:bg-[#b31a27] text-white font-bold text-sm px-5 py-[11px] rounded-lg">
            + Add user
          </button>
        </div>

        <!-- Stat cards -->
        <div class="grid grid-cols-4 gap-[18px] mb-[26px]">
          <div
            v-for="card in statCards"
            :key="card.label"
            class="bg-[#161616] border border-[#232323] rounded-xl p-5"
          >
            <div
              class="w-[38px] h-[38px] bg-[#c81e2c] rounded-lg flex items-center justify-center mb-[26px] [&>svg]:w-[18px] [&>svg]:h-[18px] [&>svg]:stroke-white [&>svg]:fill-none [&>svg]:stroke-[1.8]"
              v-html="card.icon"
            ></div>
            <div class="text-[#9b9b9b] text-[13px] mb-1.5">{{ card.label }}</div>
            <div class="text-[26px] font-extrabold">{{ card.value }}</div>
          </div>
        </div>

        <!-- Table card -->
        <div class="bg-[#161616] border border-[#232323] rounded-xl overflow-hidden">
          <div class="flex justify-between items-center px-5 py-[18px] border-b border-[#232323] gap-4 flex-wrap">
            <h3 class="text-base font-bold">All users</h3>
            <div class="flex gap-2.5">
              <input
                v-model="search"
                placeholder="Search users..."
                class="bg-[#0f0f0f] border border-[#2a2a2a] rounded-lg px-3.5 py-[9px] text-[13px] text-[#e4e4e4] placeholder-[#8a8a8a] w-60 outline-none"
              />
              <div class="bg-[#0f0f0f] border border-[#2a2a2a] rounded-lg px-3.5 py-2 text-[13px] text-[#c8c8c8] cursor-pointer">
                Role ⌄
              </div>
              <div class="bg-[#0f0f0f] border border-[#2a2a2a] rounded-lg px-3.5 py-2 text-[13px] text-[#c8c8c8] cursor-pointer">
                Status ⌄
              </div>
            </div>
          </div>

          <table class="w-full border-collapse">
            <thead class="bg-[#0f0f0f]">
              <tr>
                <th class="text-left text-[12px] text-[#8a8a8a] uppercase tracking-wide px-5 py-3 font-semibold border-b border-[#232323]">User</th>
                <th class="text-left text-[12px] text-[#8a8a8a] uppercase tracking-wide px-5 py-3 font-semibold border-b border-[#232323]">Role</th>
                <th class="text-left text-[12px] text-[#8a8a8a] uppercase tracking-wide px-5 py-3 font-semibold border-b border-[#232323]">Status</th>
                <th class="text-left text-[12px] text-[#8a8a8a] uppercase tracking-wide px-5 py-3 font-semibold border-b border-[#232323]">Joined</th>
                <th class="text-left text-[12px] text-[#8a8a8a] uppercase tracking-wide px-5 py-3 font-semibold border-b border-[#232323]">Rentals</th>
                <th class="text-left text-[12px] text-[#8a8a8a] uppercase tracking-wide px-5 py-3 font-semibold border-b border-[#232323]">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="(user, i) in filteredUsers"
                :key="user.email"
                :class="i !== filteredUsers.length - 1 ? 'border-b border-[#1c1c1c]' : ''"
              >
                <td class="px-5 py-3.5 text-sm text-[#e4e4e4]">
                  <div class="flex items-center gap-2.5">
                    <div class="w-8 h-8 rounded-full bg-[#2a2a2a] flex items-center justify-center text-xs font-bold text-[#c8c8c8] flex-shrink-0">
                      {{ user.initials }}
                    </div>
                    <div>
                      <div class="font-semibold text-white">{{ user.name }}</div>
                      <div class="text-[#8a8a8a] text-[12.5px]">{{ user.email }}</div>
                    </div>
                  </div>
                </td>
                <td class="px-5 py-3.5 text-sm">
                  <span class="text-xs px-2.5 py-1 rounded-md bg-[#232323] text-[#c8c8c8] inline-block">
                    {{ user.role }}
                  </span>
                </td>
                <td class="px-5 py-3.5 text-sm">
                  <span class="flex items-center gap-[7px] text-[13px]">
                    <span
                      class="w-[7px] h-[7px] rounded-full"
                      :class="{
                        'bg-[#3ddc78]': user.status === 'Active',
                        'bg-[#c81e2c]': user.status === 'Suspended',
                        'bg-[#e0a83e]': user.status === 'Pending'
                      }"
                    ></span>
                    {{ user.status }}
                  </span>
                </td>
                <td class="px-5 py-3.5 text-sm text-[#e4e4e4]">{{ user.joined }}</td>
                <td class="px-5 py-3.5 text-sm text-[#e4e4e4]">{{ user.rentals }}</td>
                <td class="px-5 py-3.5 text-sm">
                  <div class="flex gap-3.5 text-[#8a8a8a] text-[13px]">
                    <span class="cursor-pointer hover:text-white">Edit</span>
                    <span class="cursor-pointer hover:text-white">{{ user.secondaryAction }}</span>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>

          <div class="flex justify-between items-center px-5 py-4 text-[#8a8a8a] text-[13px]">
            <span>Showing 1–{{ users.length }} of 67 users</span>
            <div class="flex gap-1.5">
              <span class="w-7 h-7 flex items-center justify-center rounded-md border border-[#2a2a2a] cursor-pointer">‹</span>
              <span
                v-for="p in 3"
                :key="p"
                @click="currentPage = p"
                class="w-7 h-7 flex items-center justify-center rounded-md border cursor-pointer"
                :class="p === currentPage
                  ? 'bg-[#c81e2c] border-[#c81e2c] text-white'
                  : 'border-[#2a2a2a]'"
              >{{ p }}</span>
              <span class="w-7 h-7 flex items-center justify-center rounded-md border border-[#2a2a2a] cursor-pointer">›</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "UsersPage",
  data() {
    return {
      today: "Monday, July 20, 2026",
      search: "",
      currentPage: 1,
      mainNav: [
        {
          label: "Dashboard",
          icon: `<svg viewBox="0 0 24 24" stroke="currentColor" fill="none" stroke-width="1.8"><path d="M3 11l9-7 9 7"/><path d="M5 10v9a1 1 0 0 0 1 1h4v-6h4v6h4a1 1 0 0 0 1-1v-9"/></svg>`
        },
        {
          label: "Notifications",
          badge: 67,
          icon: `<svg viewBox="0 0 24 24" stroke="currentColor" fill="none" stroke-width="1.8"><path d="M18 8a6 6 0 0 0-12 0c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.7 21a2 2 0 0 1-3.4 0"/></svg>`
        },
        {
          label: "Bookings",
          icon: `<svg viewBox="0 0 24 24" stroke="currentColor" fill="none" stroke-width="1.8"><rect x="6" y="4" width="12" height="17" rx="1.5"/><rect x="9" y="2" width="6" height="3.5" rx="1"/><path d="M9 12h6M9 16h6"/></svg>`
        },
        {
          label: "Fleet",
          icon: `<svg viewBox="0 0 24 24" stroke="currentColor" fill="none" stroke-width="1.8"><path d="M13 2 4 14h6l-1 8 9-12h-6l1-8z"/></svg>`
        },
        {
          label: "Users",
          active: true,
          icon: `<svg viewBox="0 0 24 24" stroke="currentColor" fill="none" stroke-width="1.8"><circle cx="9" cy="8" r="3.2"/><path d="M3 20c0-3.5 2.7-6 6-6s6 2.5 6 6"/><circle cx="17.5" cy="9" r="2.4"/><path d="M15.8 14.3c2.3.4 4.2 2.5 4.2 5.2"/></svg>`
        }
      ],
      reportNav: [
        {
          label: "Analytics",
          icon: `<svg viewBox="0 0 24 24" stroke="currentColor" fill="none" stroke-width="1.8"><path d="M4 20V10M12 20V4M20 20v-7"/></svg>`
        },
        {
          label: "Activity logs",
          icon: `<svg viewBox="0 0 24 24" stroke="currentColor" fill="none" stroke-width="1.8"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3.5 2"/></svg>`
        }
      ],
      statCards: [
        {
          label: "Total users",
          value: 67,
          icon: `<svg viewBox="0 0 24 24"><circle cx="9" cy="8" r="3.2"/><path d="M3 20c0-3.5 2.7-6 6-6s6 2.5 6 6"/><circle cx="17.5" cy="9" r="2.4"/><path d="M15.8 14.3c2.3.4 4.2 2.5 4.2 5.2"/></svg>`
        },
        {
          label: "Active",
          value: 58,
          icon: `<svg viewBox="0 0 24 24"><path d="M20 6 9 17l-5-5"/></svg>`
        },
        {
          label: "Pending",
          value: 6,
          icon: `<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3.5 2"/></svg>`
        },
        {
          label: "Suspended",
          value: 3,
          icon: `<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M6.5 6.5l11 11"/></svg>`
        }
      ],
      users: [
        { name: "Maria Cruz", email: "maria.cruz@email.com", initials: "MC", role: "Customer", status: "Active", joined: "Jan 12, 2026", rentals: 9, secondaryAction: "Suspend" },
        { name: "Jose Reyes", email: "jose.reyes@email.com", initials: "JR", role: "Customer", status: "Active", joined: "Feb 03, 2026", rentals: 4, secondaryAction: "Suspend" },
        { name: "Angela Tan", email: "angela.tan@email.com", initials: "AT", role: "Fleet manager", status: "Pending", joined: "Jun 28, 2026", rentals: 0, secondaryAction: "Approve" },
        { name: "Ramon Dela Cruz", email: "ramon.delacruz@email.com", initials: "RD", role: "Customer", status: "Suspended", joined: "Sep 15, 2025", rentals: 2, secondaryAction: "Reactivate" },
        { name: "Liza Santos", email: "liza.santos@email.com", initials: "LS", role: "Admin", status: "Active", joined: "Nov 02, 2025", rentals: "—", secondaryAction: "Suspend" },
        { name: "Karlo Villanueva", email: "karlo.villanueva@email.com", initials: "KV", role: "Customer", status: "Active", joined: "Mar 21, 2026", rentals: 6, secondaryAction: "Suspend" }
      ]
    };
  },
  computed: {
    filteredUsers() {
      const q = this.search.trim().toLowerCase();
      if (!q) return this.users;
      return this.users.filter(
        (u) =>
          u.name.toLowerCase().includes(q) ||
          u.email.toLowerCase().includes(q)
      );
    }
  }
};
</script>